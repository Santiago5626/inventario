# Documentación de Implementación Técnica

Este documento detalla las tecnologías utilizadas en el desarrollo del sistema de inventario, así como la ubicación y lógica de las funcionalidades principales.

## 1. Stack Tecnológico

### Backend (Lógica del Servidor)
- **Framework**: Django (Python). Es el núcleo del sistema que maneja las rutas, la base de datos y la lógica de negocio.
- **Base de Datos**: 
  - *Desarrollo (Local)*: SQLite (`db.sqlite3`).
  - *Producción*: PostgreSQL (configurado vía `dj_database_url` en `settings.py`).
- **Manejo de Archivos Estáticos**: `WhiteNoise`. Permite servir archivos CSS/JS de manera eficiente en producción.

### Frontend (Interfaz de Usuario)
- **Estructura y Estilos**: HTML5 y **Bootstrap 5.3**. Se usa para el diseño responsivo (adaptable a móviles y escritorio).
- **Iconos**: **FontAwesome 6.4**. Usado para todos los iconos visuales (dashboard, botones, menú).
- **Alertas y Notificaciones**: **SweetAlert2**. Reemplaza las alertas nativas del navegador con modales estilizados y animados (ej. errores de login).
- **Gráficos**: **Chart.js**. Librería JavaScript para renderizar los gráficos de torta y barras en los dashboards.
- **Fuentes**: Google Fonts (Familia "Inter").

---

## 2. Autenticación y Usuarios

La gestión de usuarios y seguridad se encuentra en la aplicación `usuarios`.

- **Modelo de Usuario**: Se utiliza un modelo personalizado que extiende del sistema nativo de Django. Esto permite tener campos extra como el `rol`.
  - *Ubicación*: `usuarios/models.py`
- **Roles**: El sistema maneja roles definidos (`admin`, `logistica`, `lectura`, `asignador`) que determinan qué puede ver y hacer cada usuario.
- **Login**:
  - Se usa una vista personalizada `CustomLoginView` que redirige al usuario a su dashboard correspondiente según su rol después de iniciar sesión.
  - *Ubicación*: `usuarios/views.py`
- **Validación Visible**: Se implementó lógica en `login.html` que captura los errores del formulario (`form.errors`) y los muestra usando **SweetAlert2**.

---

## 3. Paneles de Control (Dashboards) y Estadísticas

La lógica de negocio principal está en la aplicación `activos`.

- **Cálculo de Estadísticas**:
  - Se utilizan consultas avanzadas del ORM de Django (`Q` objects) para filtrar activos de manera mutuamente excluyente (ej. un activo no puede estar "En Bodega" y "Asignado" a la vez para fines contables).
  - Se usan anotaciones (`annotate`) y conteos (`Count`) para agrupar datos por categoría, zona y estado.
  - *Ubicación*: `activos/views.py` (funciones `admin_dashboard`, `logistica_dashboard`, `lectura_dashboard`).
- **Visualización (Gráficos)**:
  - Los datos calculados en Python se inyectan en las plantillas HTML como objetos JSON seguros (`JSON.parse`).
  - **Chart.js** toma estos datos y renderiza los elementos `<canvas>`.
  - *Ubicación*: Bloques `<script>` al final de `admin_dashboard.html`, `logistica_dashboard.html`, etc.

## 4. Estructura de Proyecto

```bash
inventario/
├── activos/              # App principal de gestión de inventario
│   ├── models.py         # Definición de tablas (Activo, Zona, Categoria)
│   ├── views.py          # Lógica de dashboards y CRUD de activos
│   └── templates/        # Archivos HTML (vistas)
├── usuarios/             # App de gestión de usuarios y login
│   ├── models.py         # Modelo de usuario personalizado
│   └── views.py          # Lógica de login y redirección
├── static/               # Archivos CSS, JS e imágenes públicas
│   └── css/modern.css    # Estilos personalizados extra sobre Bootstrap
└── inventario_pda/       # Configuración global del proyecto (settings.py)
```

## 5. Middleware y Seguridad
En `settings.py` se configuran capas de seguridad como protección CSRF (para formularios), `SecurityMiddleware` y validación de contraseñas robustas.
