# Sistema de Inventario de Activos PDA

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Sistema web responsive para la gestión y control de inventario de equipos PDA. Diseñado para optimizar el registro, asignación y seguimiento de activos tecnológicos, garantizando una trazabilidad completa mediante roles de usuario y registros de auditoría.

---

## Características Principales

### Gestión de Accesos y Roles
El sistema adapta su interfaz según el perfil del usuario autenticado:
- **Administrador**: Control total del sistema (CRUD de activos, usuarios, reportes).
- **Logística**: Gestión de movimientos de inventario y estados.
- **Lectura/Asignador**: Vistas de consulta y reportes básicos.

### Dashboards Interactivos
Paneles de control modernos con estadísticas en tiempo real:
- **KPIs**: Total de activos, asignados, en bodega y bajas.
- **Gráficos**: Distribución por estado y categorías (Chart.js).
- **Alertas**: Notificaciones visuales de acciones y estados.

### Funcionalidades Core
- **Registro de Activos**: Formulario detallado con validaciones.
- **Trazabilidad Completa**: Historial cronológico de cambios de estado, ubicación y responsable.
- **Auditoría**: Registro automático de quién modificó qué y cuándo.
- **Reportes Avanzados**: Exportación a Excel y filtrado por sedes.
- **Gestión de Ubicaciones**: Control de zonas y sedes.

---

## Estructura del Proyecto

```text
inventario_pda/
├── activos/                # Módulo principal de lógica de negocio
│   ├── models.py           # Definición de datos (Activo, Trazabilidad)
│   ├── views.py            # Controladores de vistas y dashboards
│   ├── urls.py             # Rutas de la aplicación
│   └── templates/          # Plantillas HTML/Django
├── usuarios/               # Gestión de autenticación y perfiles
├── static/                 # Recursos frontend (Modern CSS, JS, imágenes)
├── templates/              # Plantillas base y componentes globales
└── manage.py               # CLI de Django
```

---

## Instalación y Despliegue

### Requisitos Previos
- Python 3.10+
- Git
- PostgreSQL

### Configuración Local

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd inventario
   ```

2. **Crear entorno virtual e instalar dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar base de datos:**
   Asegúrate de tener una instancia de PostgreSQL corriendo y configura las variables de entorno necesarias.
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Ejecutar servidor:**
   ```bash
   python manage.py runserver
   ```
   Accede a: `http://127.0.0.1:8000/`

---

## Despliegue en Producción (Linux VM)

El proyecto está preparado para desplegarse de manera robusta usando Nginx, Gunicorn y Systemd en distribuciones basadas en Ubuntu/Debian.

### 1. Instalación de Base
Ejecuta el script de instalación para preparar los paquetes nativos de Ubuntu:
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

### 2. Configuración de Entorno
Clona la plantilla `.env.example` y define tus variables:
```bash
cp .env.example .env
nano .env
```

**Guía de Variables en el `.env`:**
- **`DEBUG`**: En producción siempre debe ser `False`.
- **`SECRET_KEY`**: Genera una clave nueva y única desde la consola de Linux usando:
  `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- **`ALLOWED_HOSTS`**: Separa por comas la dirección IP del servidor y/o el dominio comprado (ej: `127.0.0.1,200.5.4.3,miservicio.com`).
- **`DATABASE_URL`**: Contiene la contraseña del usuario de base de datos de PostgreSQL creado en el siguiente paso. Formato: `postgresql://USUARIO:CONTRASEÑA@127.0.0.1:5432/inventario_db`
- **`CSRF_TRUSTED_ORIGINS`**: Los mismos que pusiste en host, pero con `http://` o `https://` al inicio (ej: `http://200.5.4.3,https://miservicio.com`).

### 3. Ejecución como Servicio con Systemd
Crea el servicio para Gunicorn en `/etc/systemd/system/inventario.service`:
```ini
[Unit]
Description=Gunicorn daemon for Inventario
After=network.target

[Service]
User=tu_usuario_linux
Group=www-data
WorkingDirectory=/ruta/a/tu/inventario
ExecStart=/ruta/a/tu/inventario/venv/bin/gunicorn --workers 3 --bind unix:/ruta/a/tu/inventario/inventario.sock inventario_pda.wsgi:application

[Install]
WantedBy=multi-user.target
```

Inicia Gunicorn de forma constante:
```bash
sudo systemctl enable --now inventario
```

### 4. Configuración del Proxy Inverso con Nginx
Crea un bloque en `/etc/nginx/sites-available/inventario`:
```nginx
server {
    listen 80;
    server_name tu_dominio_o_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /ruta/a/tu/inventario;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/ruta/a/tu/inventario/inventario.sock;
    }
}
```

Habilita el sitio y reinicia Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/inventario /etc/nginx/sites-enabled
sudo systemctl restart nginx
```
---

## Tecnologías

- **Backend:** Django 5.x
- **Frontend:** Bootstrap 5, FontAwesome 6, Modern CSS (Custom)
- **Visualización:** Chart.js
- **Base de Datos:** PostgreSQL
- **Servidor:** Gunicorn

---

Desarrollado para optimizar la gestión de recursos tecnológicos.
