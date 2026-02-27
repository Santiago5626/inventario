#!/bin/bash

# Configuración
FECHA=$(date +%Y-%m-%d_%H-%M-%S)
BASE_DATOS="inventario_db"
USUARIO="postgres"
DESTINO="/home/soporte/backups"

# Crear directorio si no existe
mkdir -p $DESTINO

# Ejecutar el backup
# Usamos sudo -u postgres para evitar problemas de permisos
sudo -u postgres pg_dump $BASE_DATOS > $DESTINO/backup_${BASE_DATOS}_${FECHA}.sql

# Borrar backups mayores a 30 dias
find $DESTINO -type f -name "*.sql" -mtime +30 -delete

echo "Backup de $BASE_DATOS completado en $DESTINO/backup_${BASE_DATOS}_${FECHA}.sql"
