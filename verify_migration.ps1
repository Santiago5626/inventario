# Script de Verificacion Rapida Post-Migracion

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICACION DE MIGRACION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cargar variables de entorno
Get-Content .env.migration | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

Write-Host "Ejecutando verificacion de datos..." -ForegroundColor Yellow
Write-Host ""

# Crear script de Python temporal para verificacion
$pythonScript = @"
from activos.models import Activo, Tranzabilidad, Ubicacion, Categoria, Marca
from usuarios.models import Usuario
from django.contrib.auth.models import Group

print("=" * 60)
print("CONTEO DE REGISTROS EN LA NUEVA BASE DE DATOS")
print("=" * 60)
print()

# Usuarios
total_usuarios = Usuario.objects.count()
print(f"OK - Usuarios: {total_usuarios}")

# Grupos
total_grupos = Group.objects.count()
print(f"OK - Grupos: {total_grupos}")

# Activos
total_activos = Activo.objects.count()
print(f"OK - Activos: {total_activos}")

# Tranzabilidad
total_tranzabilidad = Tranzabilidad.objects.count()
print(f"OK - Registros de Tranzabilidad: {total_tranzabilidad}")

# Ubicaciones
total_ubicaciones = Ubicacion.objects.count()
print(f"OK - Ubicaciones: {total_ubicaciones}")

# Categorias
total_categorias = Categoria.objects.count()
print(f"OK - Categorias: {total_categorias}")

# Marcas
total_marcas = Marca.objects.count()
print(f"OK - Marcas: {total_marcas}")

print()
print("=" * 60)
print()

# Verificar integridad
print("VERIFICACION DE INTEGRIDAD")
print("=" * 60)
print()

activos_sin_ubicacion = Activo.objects.filter(ubicacion__isnull=True).count()
if activos_sin_ubicacion == 0:
    print(f"OK - Todos los activos tienen ubicacion asignada")
else:
    print(f"ADVERTENCIA - Activos sin ubicacion: {activos_sin_ubicacion}")

tranz_sin_activo = Tranzabilidad.objects.filter(activo__isnull=True).count()
if tranz_sin_activo == 0:
    print(f"OK - Todas las tranzabilidades tienen activo asignado")
else:
    print(f"ADVERTENCIA - Tranzabilidades sin activo: {tranz_sin_activo}")

tranz_sin_usuario = Tranzabilidad.objects.filter(usuario__isnull=True).count()
if tranz_sin_usuario == 0:
    print(f"OK - Todas las tranzabilidades tienen usuario asignado")
else:
    print(f"ADVERTENCIA - Tranzabilidades sin usuario: {tranz_sin_usuario}")

print()
print("=" * 60)
print()

# Verificar migraciones
print("ESTADO DE MIGRACIONES")
print("=" * 60)
print()
from django.core.management import call_command
call_command('showmigrations', '--list')

print()
print("=" * 60)
print("VERIFICACION COMPLETADA")
print("=" * 60)
"@

$pythonScript | Out-File -FilePath "verify_migration.py" -Encoding utf8

# Ejecutar verificacion
Get-Content verify_migration.py | python manage.py shell

# Limpiar archivo temporal
Remove-Item "verify_migration.py" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICACION COMPLETADA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
