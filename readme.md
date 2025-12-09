# 📦 Sistema de Inventario de Activos PDA

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

Sistema web responsive para la gestión y control de inventario de equipos PDA. Diseñado para optimizar el registro, asignación y seguimiento de activos tecnológicos, garantizando una trazabilidad completa mediante roles de usuario y registros de auditoría.

---

## 🚀 Características Principales

### 🔐 Gestión de Accesos y Roles
El sistema adapta su interfaz según el perfil del usuario autenticado:
- **Administrador**: Control total del sistema (CRUD de activos, usuarios, reportes).
- **Logística**: Gestión de movimientos de inventario y estados.
- **Lectura/Asignador**: Vistas de consulta y reportes básicos.

### 📊 Dashboards Interactivos
Paneles de control modernos con estadísticas en tiempo real:
- **KPIs**: Total de activos, asignados, en bodega y bajas.
- **Gráficos**: Distribución por estado y categorías (Chart.js).
- **Alertas**: Notificaciones visuales de acciones y estados.

### 🛠 Funcionalidades Core
- **Registro de Activos**: Formulario detallado con validaciones.
- **Trazabilidad Completa**: Historial cronológico de cambios de estado, ubicación y responsable.
- **Auditoría**: Registro automático de quién modificó qué y cuándo.
- **Reportes Avanzados**: Exportación a Excel y filtrado por sedes.
- **Gestión de Ubicaciones**: Control de zonas y sedes.

---

## 📂 Estructura del Proyecto

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
├── db.sqlite3              # Base de datos local
└── manage.py               # CLI de Django
```

---

## 💻 Instalación y Despliegue

### Requisitos Previos
- Python 3.10+
- Git

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

## ☁️ Despliegue (Render)

El proyecto está configurado para despliegue automático en Render mediante `render.yaml`.

**Comando de Build:**
```bash
pip install -r requirements.txt
```

**Comando de Inicio:**
```bash
gunicorn inventario_pda.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🎨 Tecnologías

- **Backend:** Django 5.x
- **Frontend:** Bootstrap 5, FontAwesome 6, Modern CSS (Custom)
- **Visualización:** Chart.js
- **Base de Datos:** SQLite (Dev/Prod simple)
- **Servidor:** Gunicorn

---

Desarrollado para optimizar la gestión de recursos tecnológicos. 
