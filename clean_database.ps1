# Script para limpiar tranzabilidades de la base de datos
# Esto permite reimportar activos sin conflictos

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA DE TRANZABILIDADES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cargar variables de entorno
Get-Content .env.migration | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

Write-Host "ADVERTENCIA: Este script eliminara TODAS las tranzabilidades" -ForegroundColor Red
Write-Host "de la base de datos para permitir la reimportacion de activos." -ForegroundColor Red
Write-Host ""
Write-Host "Deseas continuar? (S/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -ne "S" -and $response -ne "s") {
    Write-Host "Operacion cancelada" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Eliminando tranzabilidades..." -ForegroundColor Yellow

# Crear script de Python para eliminar tranzabilidades
$pythonScript = @"
from activos.models import Tranzabilidad

print("Contando tranzabilidades actuales...")
total_antes = Tranzabilidad.objects.count()
print(f"Total de tranzabilidades: {total_antes}")
print()

if total_antes > 0:
    print("Eliminando todas las tranzabilidades...")
    Tranzabilidad.objects.all().delete()
    print("OK - Tranzabilidades eliminadas")
    
    total_despues = Tranzabilidad.objects.count()
    print(f"Total de tranzabilidades restantes: {total_despues}")
else:
    print("No hay tranzabilidades para eliminar")
"@

$pythonScript | Out-File -FilePath "clean_tranzabilidades.py" -Encoding utf8

# Ejecutar limpieza
Get-Content clean_tranzabilidades.py | python manage.py shell

# Limpiar archivo temporal
Remove-Item "clean_tranzabilidades.py" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "La base de datos esta lista para recibir los activos." -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. Importa los activos desde tu fuente de datos" -ForegroundColor White
Write-Host "2. Una vez importados los activos, podras registrar nuevas tranzabilidades" -ForegroundColor White
Write-Host ""
