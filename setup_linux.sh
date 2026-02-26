#!/bin/bash
# ==========================================================
# Script de Instalación para Entorno de Producción (Linux)
# ==========================================================
# Este script está pensado para ejecutarse en Ubuntu/Debian.

echo "=========================================================="
echo "Iniciando instalación de dependencias del sistema operativo"
echo "=========================================================="

# 1. Actualizar repositorios e instalar paquetes base del sistema
sudo apt update
sudo apt install -y python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl

echo "=========================================================="
echo "Configurando Entorno Virtual Python..."
echo "=========================================================="

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Actualizar pip e instalar dependencias del proyecto
echo "Instalando dependencias de Python desde requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "=========================================================="
echo "Instalación completada."
echo "=========================================================="
echo ""
echo "Siguientes Pasos (Sigue la guía del README.md):"
echo "1. Configurar la base de datos PostgreSQL."
echo "2. Copiar .env.example a .env y llenar los datos reales."
echo "3. Ejecutar migraciones (python manage.py migrate)."
echo "4. Recolectar estáticos (python manage.py collectstatic)."
echo "5. Configurar los servicios systemd y Nginx."
echo ""
