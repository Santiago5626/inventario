# Script de Migracion a Nueva Base de Datos
# Este script ejecuta las migraciones y la importacion de datos

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MIGRACION A NUEVA BASE DE DATOS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cargar variables de entorno desde .env.migration
Write-Host "[1/5] Cargando configuracion..." -ForegroundColor Yellow
Get-Content .env.migration | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
        Write-Host "  OK - $name configurado" -ForegroundColor Green
    }
}
Write-Host ""

# Verificar conexion a la base de datos
Write-Host "[2/5] Verificando conexion a la base de datos..." -ForegroundColor Yellow
python manage.py check --database default
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR - No se pudo conectar con la base de datos" -ForegroundColor Red
    Write-Host "  Verifica que la URL de la base de datos sea correcta" -ForegroundColor Red
    exit 1
}
Write-Host "  OK - Conexion exitosa" -ForegroundColor Green
Write-Host ""

# Ejecutar migraciones
Write-Host "[3/5] Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR - No se pudieron ejecutar las migraciones" -ForegroundColor Red
    exit 1
}
Write-Host "  OK - Migraciones completadas" -ForegroundColor Green
Write-Host ""

# Verificar si existe el archivo de backup
Write-Host "[4/5] Verificando archivo de backup..." -ForegroundColor Yellow
if (Test-Path "db_dump.json") {
    Write-Host "  OK - Archivo db_dump.json encontrado" -ForegroundColor Green
    $fileSize = (Get-Item "db_dump.json").Length / 1KB
    Write-Host "  Tamanio: $([math]::Round($fileSize, 2)) KB" -ForegroundColor Cyan
}
else {
    Write-Host "  ERROR - Archivo db_dump.json NO encontrado" -ForegroundColor Red
    Write-Host "  Debes exportar los datos primero desde la base de datos antigua" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Deseas continuar sin importar datos? (S/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -ne "S" -and $response -ne "s") {
        Write-Host "  Migracion cancelada" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Importar datos
if (Test-Path "db_dump.json") {
    Write-Host "[5/5] Importando datos..." -ForegroundColor Yellow
    Write-Host "  Esto puede tomar varios minutos dependiendo del tamanio de los datos" -ForegroundColor Cyan
    Get-Content import_data.py | python manage.py shell
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR - No se pudieron importar los datos" -ForegroundColor Red
        exit 1
    }
    Write-Host "  OK - Datos importados exitosamente" -ForegroundColor Green
}
else {
    Write-Host "[5/5] Importacion de datos omitida" -ForegroundColor Yellow
}
Write-Host ""

# Resumen
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MIGRACION COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. Verificar los datos en la nueva base de datos" -ForegroundColor White
Write-Host "2. Configurar DATABASE_URL en Render con la URL interna:" -ForegroundColor White
Write-Host "   postgresql://inventario2_r5j0_user:z4HPFs0bIVNt4SgF31jbS9IgH2tXWSnQ@dpg-d5j6aj6uk2gs73dqb7dg-a/inventario2_r5j0" -ForegroundColor Cyan
Write-Host "3. Redesplegar el servicio en Render" -ForegroundColor White
Write-Host "4. Ejecutar las verificaciones post-migracion" -ForegroundColor White
Write-Host ""
