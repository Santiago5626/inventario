from django.db import migrations

def enforce_schema(apps, schema_editor):
    Categoria = apps.get_model('activos', 'Categoria')
    Marca = apps.get_model('activos', 'Marca')
    Activo = apps.get_model('activos', 'Activo')

    # Lista permitida
    allowed_categories = ['MAQUINAS']
    allowed_marcas = [
        'SUNMI V1',
        'SUNMI V2',
        'SUNMI V2 PRO',
        'N910',
        'N910 GRIS',
    ]

    # 1. Asegurar que exista la categoría MAQUINAS
    maquinas_cat, _ = Categoria.objects.get_or_create(
        nombre='MAQUINAS',
        defaults={'descripcion': 'Categoría principal para máquinas'}
    )

    # 2. Mover o Crear Marcas permitidas
    for marca_nombre in allowed_marcas:
        # Buscar si ya existe (podría estar en otra categoría)
        marca = Marca.objects.filter(nombre=marca_nombre).first()
        if marca:
            # Si existe, asegurar que esté en MAQUINAS
            if marca.categoria != maquinas_cat:
                marca.categoria = maquinas_cat
                marca.save()
        else:
            # Si no existe, crearla
            Marca.objects.create(
                nombre=marca_nombre,
                categoria=maquinas_cat,
                descripcion=f'Marca autogenerada {marca_nombre}'
            )

    # 3. Eliminar Marcas NO permitidas
    # Primero desasociar activos para evitar borrado en cascada no deseado (o dejar que se borre si es CASCADE)
    # El modelo Marca tiene on_delete=models.CASCADE en su relación con Categoria?
    # No, en Activo.marca es on_delete=models.SET_NULL (visto en models.py linea 57)
    # Pero Marca.categoria es CASCADE.
    
    # Eliminar marcas que no están en la lista permitida
    Marca.objects.exclude(nombre__in=allowed_marcas).delete()

    # 4. Eliminar Categorías NO permitidas
    # Esto borrará en cascada las marcas que estén en esas categorías (si quedara alguna, pero ya borramos marcas)
    Categoria.objects.exclude(nombre__in=allowed_categories).delete()


def reverse_enforce(apps, schema_editor):
    # No hay reversión fácil exacta para recuperación de datos borrados.
    # Podríamos recrear 'Dispositivos' si se quisiera, pero dejémoslo simple.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('activos', '0017_populate_centro_costo'),
    ]

    operations = [
        migrations.RunPython(enforce_schema, reverse_enforce),
    ]
