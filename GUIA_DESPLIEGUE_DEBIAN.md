# Guía Completa de Despliegue: Sistema de Inventario en Debian

Esta guía detalla el proceso realizado para desplegar el Sistema de Inventario de Activos PDA en una máquina virtual con Debian desde cero. Se incluyen explicaciones sobre la importancia de cada paso.

---

## 1. Preparación del Sistema Operativo
Se requiere una instalación limpia de Debian con acceso root.

1. **Actualización básica**:
   ```bash
   apt update && apt upgrade -y
   apt install git -y
   ```
   > [!NOTE]
   > Mantener el sistema actualizado previene fallos de seguridad y asegura que las librerías de Python se compilen correctamente.

2. **Herramientas de red y configuración de IP**:
    Si la máquina no recibe IP (DHCP desactivado o fallo de `dhclient`), se debe configurar una IP estática.
    
    *Configuración temporal (para pruebas rápidas):*
    ```bash
    ip addr add 192.168.155.200/24 dev enp0s3
    ip link set enp0s3 up
    ip route add default via 192.168.155.1
    ```

    *Configuración permanente (editar /etc/network/interfaces):*
    ```bash
    nano /etc/network/interfaces
    ```
    Configuración recomendada para la interfaz (ej. `enp0s3`):
    ```text
    auto enp0s3
    iface enp0s3 inet static
        address 192.168.155.200
        netmask 255.255.255.0
        gateway 192.168.155.1
        dns-nameservers 8.8.8.8 8.8.4.4
    ```
    > [!IMPORTANT]
    > Sin una IP fija o correctamente asignada por DHCP, el servidor no será accesible. Si tu red local no tiene DHCP activo (como en este caso), la configuración estática es obligatoria.

---

## 2. Configuración del Proyecto y Dependencias

1. **Clonación del código**:
   ```bash
   git clone <URL_DEL_REPOSITORIO> /home/soporte/inventario
   cd /home/soporte/inventario
   ```

2. **Instalación de herramientas de compilación**:
   Modificamos `setup_linux.sh` para incluir `build-essential`. Esto es vital porque la librería de PostgreSQL para Python (`psycopg2`) necesita compilar código en C durante la instalación.
   ```bash
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```

3. **Compatibilidad con Python 3.13**:
   Debian Trixie usa Python 3.13. Las versiones antiguas de `psycopg2` fallan en este entorno.
   *Solución aplicada en `requirements.txt`:*
   ```text
   psycopg2-binary>=2.9.10
   ```
   > [!TIP]
   > Siempre verifica que las librerías binarias sean compatibles con versiones muy recientes de Python para evitar errores de "Build wheel".

---

## 3. Base de Datos (PostgreSQL)

1. **Creación de usuario y DB**:
   ```bash
   sudo -u postgres psql
   ```
   Dentro de psql:
   ```sql
   CREATE DATABASE inventario_db;
   CREATE USER admin WITH PASSWORD 'admin';
   GRANT ALL PRIVILEGES ON DATABASE inventario_db TO admin;
   \q
   ```
   > [!WARNING]
   > Aunque usamos 'admin/admin' para pruebas, en un servidor expuesto a internet se deben usar contraseñas robustas.

---

## 4. Configuración de Django (.env)

1. **Variables críticas**:
   - `DEBUG=True`: Útil durante el despliegue para ver errores, pero debe ser `False` en producción real.
   - `ALLOWED_HOSTS=*`: Permite que cualquier IP acceda al sistema. Es necesario cuando la IP del servidor es asignada por DHCP y puede cambiar.

2. **Inicialización**:
   ```bash
   source venv/bin/activate
   python manage.py makemigrations activos
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

---

## 5. Puesta en Producción Local

### Gunicorn (Systemd)
Gunicorn es el servidor que realmente ejecuta el código Python. Lo configuramos como servicio para que:
1. Arranque solo al encender la VM.
2. Se reinicie automáticamente si falla.
3. No dependa de una terminal abierta.

### Nginx (Proxy Inverso)
Nginx actúa como "la cara" del servidor. Recibe las peticiones en el puerto 80 y las pasa a Gunicorn.
- **¿Por qué Nginx?**: Porque maneja archivos estáticos (CSS, Imágenes) de forma mucho más eficiente que un servidor Python y añade una capa de seguridad.

> [!IMPORTANT]
> **Permisos de carpeta**: Ejecutamos `sudo chmod 755 /home/soporte`. Sin esto, Nginx no podrá leer el archivo `.sock` dentro de tu carpeta de usuario y dará error 502.

---

## 6. Acceso desde la Red
Si usas **VirtualBox**:
1. Cambia la Red a **Adaptador Puente** (Bridged Adapter).
2. Esto hace que la VM sea un dispositivo más en tu WiFi/Cable, tal como si fuera otro laptop físico.

**Acceso final:** `http://<IP_DE_LA_VM>` (Ejemplo: `http://192.168.155.200`)
