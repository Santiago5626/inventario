import sys
from django.core import serializers
from django.db import transaction, IntegrityError

def import_data():
    print("Iniciando importacion (v2)...", file=sys.stderr, flush=True)
    try:
        with open('db_dump.json', 'r', encoding='utf-8') as f:
            data = f.read()
            
        objects = serializers.deserialize('json', data, ignorenonexistent=True)
        
        count = 0
        skipped = 0
        for obj in objects:
            try:
                obj.save()
                count += 1
                if count % 10 == 0:
                    print(f"Importados {count} objetos...", file=sys.stderr, flush=True)
            except IntegrityError as e:
                # Skip duplicates
                skipped += 1
                # print(f"Salatado por duplicado: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error en objeto {obj}: {e}", file=sys.stderr, flush=True)
                    
        print(f"Importacion finalizada. Total importados: {count}, Saltados: {skipped}", file=sys.stderr, flush=True)
        
    except Exception as e:
        print(f"Error FATAL: {e}", file=sys.stderr, flush=True)

import_data()
