# Guía Completa de Despliegue: Sistema de Inventario en Debian

Esta guía detalla el proceso realizado para desplegar el Sistema de Inventario de Activos PDA en una máquina virtual con Debian desde cero.

---

## 1. Preparación del Sistema Operativo
Se requiere una instalación limpia de Debian con acceso root.

1. **Actualización básica**:
   ```bash
   apt update && apt upgrade -y
   apt install git -y
   ```

2. **Herramientas de red**: (Si no tienes IP en modo puente)
   ```bash
   apt install isc-dhcp-client -y
   dhclient enp0s3
   ```

---

## 2. Configuración del Proyecto y Dependencias

1. **Clonación del código**:
   ```bash
   git clone <URL_DEL_REPOSITORIO> /home/soporte/inventario
   cd /home/soporte/inventario
   ```

2. **Instalación automatizada**:
   Se utilizó el script `setup_linux.sh` modificado para incluir herramientas de compilación necesarias para Python 3.13:
   ```bash
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```
   *Nota: El script instala Python, PostgreSQL y Nginx.*

3. **Corrección de psycopg2**:
   Para Python 3.13, se debe usar una versión compatible en `requirements.txt`:
   ```text
   psycopg2-binary>=2.9.10
   ```

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

---

## 4. Configuración de Django (.env)

1. **Crear archivo de entorno**:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. **Variables críticas**:
   ```env
   DEBUG=True
   SECRET_KEY=tu_clave_aleatoria
   ALLOWED_HOSTS=*
   DATABASE_URL=postgresql://admin:admin@localhost:5432/inventario_db
   ```

3. **Inicialización**:
   ```bash
   source venv/bin/activate
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

---

## 5. Puesta en Producción Local

### Gunicorn (Systemd)
Crea el archivo `/etc/systemd/system/inventario.service`:
```ini
[Unit]
Description=Gunicorn daemon for Inventario
After=network.target

[Service]
User=soporte
Group=www-data
WorkingDirectory=/home/soporte/inventario
ExecStart=/home/soporte/inventario/venv/bin/gunicorn --workers 3 --bind unix:/home/soporte/inventario/inventario.sock inventario_pda.wsgi:application

[Install]
WantedBy=multi-user.target
```
Habilitar: `sudo systemctl enable --now inventario`

### Nginx (Proxy Inverso)
Crea el archivo `/etc/nginx/sites-available/inventario`:
```nginx
server {
    listen 80;
    server_name _; # Acepta cualquier IP

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ { root /home/soporte/inventario; }
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/soporte/inventario/inventario.sock;
    }
}
```
Activar:
```bash
sudo ln -sf /etc/nginx/sites-available/inventario /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo chmod 755 /home/soporte
sudo systemctl restart nginx
```

---

## 6. Acceso desde la Red
Si usas **VirtualBox**:
1. Cambia la Red a **Adaptador Puente** (Bridged Adapter).
2. Obtén la IP corporativa: `ip addr`.
3. Accede desde cualquier dispositivo usando el navegador: `http://<IP_DE_LA_VM>`.
