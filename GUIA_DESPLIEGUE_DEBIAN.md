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

1. **Creación de usuario, DB y permisos**:
   ```bash
   sudo -u postgres psql
   ```
   Dentro de psql, ejecuta cada línea **por separado**:
   ```sql
   CREATE DATABASE inventario_db;
   CREATE USER admin WITH PASSWORD 'admin';
   GRANT ALL PRIVILEGES ON DATABASE inventario_db TO admin;
   ALTER DATABASE inventario_db OWNER TO admin;
   GRANT ALL ON SCHEMA public TO admin;
   \q
   ```
   > [!WARNING]
   > Aunque usamos 'admin/admin' para pruebas, en un servidor expuesto a internet se deben usar contraseñas robustas.

   > [!IMPORTANT]
   > **PostgreSQL 15+**: A partir de esta versión, los permisos sobre el esquema `public` no se otorgan automáticamente. Si se omite el `GRANT ALL ON SCHEMA public TO admin`, Django no podrá crear tablas y el comando `migrate` fallará con `permission denied for schema public`.

---

## 4. Configuración de Django (.env)

1. **Variables del archivo `.env`**:
   El archivo `.env` debe estar dentro de `/home/soporte/inventario/`. Las variables obligatorias son:
   ```text
   DEBUG=False
   SECRET_KEY=<clave_secreta_larga>
   ALLOWED_HOSTS=192.168.155.200,localhost,127.0.0.1
   DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario_db
   CSRF_TRUSTED_ORIGINS=http://192.168.155.200
   ```
   > [!IMPORTANT]
   > El proyecto usa `python-dotenv` para cargar este archivo automáticamente. Si no, Django usa SQLite por defecto aunque `DATABASE_URL` esté configurado.

   > [!WARNING]
   > `CSRF_TRUSTED_ORIGINS` no acepta el comodín `*` en Django 4.0+. Siempre debe incluir el esquema (`http://` o `https://`).

2. **Inicialización**:
   ```bash
   source venv/bin/activate
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

> [!IMPORTANT]
> El servicio systemd para este proyecto se llama **`inventario.service`**, no `gunicorn.service`. Usa siempre:
> ```bash
> sudo systemctl restart inventario.service
> sudo systemctl status inventario.service
> ```

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

---

## 7. Exportación y Portabilidad (Migración)
Si deseas llevar esta máquina virtual con **todas sus configuraciones** (Gunicorn, Nginx, PostgreSQL, Backups) a otra computadora:

### En la máquina de origen (VirtualBox):
1.  Apaga la VM completamente.
2.  Ve a **Archivo > Exportar servicio virtualizado** (Export Appliance).
3.  Selecciona la VM "Debian" y elige el formato **OVA**.
4.  Guarda el archivo `.ova` en un pendrive o disco externo.

### En la máquina de destino:
1.  Abre VirtualBox y ve a **Archivo > Importar servicio virtualizado**.
2.  Selecciona el archivo `.ova`.
3.  **IMPORTANTE**: En la configuración de importación, selecciona **"Reiniciar la dirección MAC de todas las tarjetas de red"**.
4.  Una vez importada, verifica en la pestaña **Red** que el Adaptador siga en modo **Adaptador Puente**.

### Migración a Hyper-V (Consideraciones Especiales)
Si conviertes el disco a `.vhd` para usarlo en Hyper-V:
1.  **Conmutador Virtual**: En la configuración de la VM en Hyper-V, asegúrate de conectar el Adaptador de Red a un conmutador de tipo **Externo**.
2.  **Interfaz eth0**: Hyper-V suele renombrar la tarjeta a `eth0`. Debes editar `/etc/network/interfaces` y reemplazar `enp0s3` por `eth0`.
3.  **NO-CARRIER**: Si ves este error en `ip addr`, revisa que el cable virtual esté "conectado" en la configuración de Hyper-V.

> [!NOTE]
> Al cambiar de computadora/red, la IP de la VM podría cambiar si el router es diferente. Asegúrate de actualizar el archivo `.env` y la IP estática en `/etc/network/interfaces` si es necesario para que coincida con el rango de la nueva red.
