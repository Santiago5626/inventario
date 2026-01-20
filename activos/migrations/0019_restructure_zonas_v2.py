from django.db import migrations

def restructure_zonas(apps, schema_editor):
    Zona = apps.get_model('activos', 'Zona')
    CentroCosto = apps.get_model('activos', 'CentroCosto')

    # 1. Eliminar todas las zonas existentes para iniciar limpio
    Zona.objects.all().delete()

    # 2. Crear Zona VALLEDUPAR explícitamente
    valledupar_zone = Zona.objects.create(
        nombre='VALLEDUPAR',
        codigo='66666'
    )

    # 3. Iterar sobre Centros de Costo
    for cc in CentroCosto.objects.all():
        nombre_cc = cc.nombre.upper().strip()
        
        # Si inicia con VALLEDUPAR, ya está cubierto por la zona creada arriba (se agrupan)
        if nombre_cc.startswith('VALLEDUPAR'):
            continue
        
        # Para los demás, crear una zona con el mismo nombre y código
        # Usamos get_or_create para evitar duplicados si hay múltiples centros de costo con mismo nombre (poco probable si es único en CC)
        Zona.objects.get_or_create(
            nombre=cc.nombre,
            defaults={'codigo': cc.codigo}
        )

def reverse_restructure(apps, schema_editor):
    # Reversión: Borrar todo.
    Zona = apps.get_model('activos', 'Zona')
    Zona.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('activos', '0018_cleanup_and_enforce_schema'),
    ]

    operations = [
        migrations.RunPython(restructure_zonas, reverse_restructure),
    ]
