# KI: Seguridad en Despliegue Local (Debian + Django)

Este Item de Conocimiento (KI) resume las capas de seguridad implementadas en el servidor local de inventario para proteger los datos y la integridad del sistema.

## 1. Seguridad a Nivel de Sistema Operativo (Debian)

- **Usuario de Aplicación No Pervilegiado**: El servicio Gunicorn corre bajo el usuario `soporte` y el grupo `www-data`. Esto limita el daño potencial si la aplicación fuera comprometida, ya que no tiene acceso total al sistema (root).
- **Control de Permisos**: La carpeta `/home/soporte` se configuró con permisos `755` para permitir que Nginx acceda al socket de comunicación, pero manteniendo la estructura de archivos protegida.
- **Gestión de Servicios con Systemd**: El uso de archivos `.service` permite un control estricto sobre cómo se inician y ejecutan las aplicaciones, evitando procesos huérfanos.

## 2. Seguridad en la Capa de Servidor Web (Nginx)

- **Proxy Inverso**: Nginx actúa como escudo frente a Gunicorn. Esto oculta los detalles internos de la aplicación Django.
- **Restricción de Acceso Local**: Por defecto, el servidor está configurado para escuchar en el puerto 80, pero el acceso externo está controlado por el modo de red de la máquina virtual (NAT o Puente).

## 3. Seguridad de la Aplicación (Django)

- **Variables de Entorno (.env)**: La información sensible (`SECRET_KEY`, credenciales de DB) nunca se escribe directamente en el código. Se cargan dinámicamente desde el archivo `.env`.
- **Middleware de Seguridad**: Se utilizan los componentes estándar de Django para prevenir ataques comunes:
  - `SecurityMiddleware`: Mejora la seguridad en las cabeceras HTTP.
  - `CsrfViewMiddleware`: Protege contra ataques de falsificación de petición en sitios cruzados.
  - `XFrameOptionsMiddleware`: Previene ataques de Clickjacking.
- **Autenticación Case-Insensitive**: Se implementó un backend personalizado para asegurar que los nombres de usuario no sean duplicados por diferencias de mayúsculas/minúsculas.

## 4. Seguridad de Red (VirtualBox)

- **Modo NAT + Reenvío**: En la fase inicial, el servidor es "invisible" para la red externa, permitiendo pruebas seguras a través de un túnel específico (`localhost:8080`).
- **Adaptador Puente**: Al pasar a producción local, la máquina virtual recibe su propia IP en el rango empresarial (`192.168.155.x`), lo que requiere vigilancia sobre quién tiene acceso físico o vía WiFi a esa red.

## 5. Recomendaciones de Fortalecimiento (Hardening)

Para una seguridad aún mayor, se recomienda:
1.  **Activación de Firewall (UFW)**: Instalar `ufw` y permitir solo los puertos `80` (Nginx) y `22` (SSH si es necesario).
2.  **HTTPS Local**: Generar un certificado auto-firmado y configurarlo en Nginx para encriptar los datos incluso dentro de la red local.
3.  **Contraseñas de Base de Datos**: Cambiar la clave `admin/admin` por una generada aleatoriamente en el archivo `.env` y en PostgreSQL.

---
*Este KI sirve como referencia para mantener la integridad del servidor en entornos corporativos.*
