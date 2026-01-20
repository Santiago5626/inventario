import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario.settings")
django.setup()

from activos.models import Marca, Activo, Categoria

print(f"Marcas: {Marca.objects.count()}")
print(f"Categorias: {Categoria.objects.count()}")
print(f"Cargos: {len(list(Activo.objects.values_list('cargo', flat=True).distinct()))}")
print(f"Operadores: {len(list(Activo.objects.values_list('operador', flat=True).distinct()))}")
print(f"Estados: {len(list(Activo.objects.values_list('estado', flat=True).distinct()))}")

# Check sample values
print("Sample Marcas:", list(Marca.objects.values_list('nombre', flat=True)[:5]))
