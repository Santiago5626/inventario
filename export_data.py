import sys
from django.core import serializers
from django.apps import apps

def export():
    print("Iniciando exportacion...", file=sys.stderr)
    try:
        # Apps to dump
        target_apps = ['usuarios', 'activos']
        
        objects = []
        for app_label in target_apps:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                qs = model.objects.all()
                count = qs.count()
                print(f"Exportando {model.__name__}: {count} objetos", file=sys.stderr)
                objects.extend(list(qs))
        
        # Serialize to JSON
        # Using natural keys to avoid ID conflicts or dependency issues where possible
        json_data = serializers.serialize('json', objects, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        
        with open('db_dump.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
            
        print("Exportacion completada exitosamente a db_dump.json", file=sys.stderr)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

export()
