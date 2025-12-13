import os
import django
from django.db import connection

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_pda.settings')
django.setup()

def fix_sequences():
    print(f"Vendor: {connection.vendor}")
    if connection.vendor != 'postgresql':
        print("Este script está diseñado para PostgreSQL. Tu base de datos actual es:", connection.vendor)
        print("Si estás usando SQLite, este error debió ser diferente (UNIQUE constraint failed).")
        print("Por favor verifica si tienes una variable de entorno DATABASE_URL configurada.")
        return

    print("Iniciando reparación de secuencias...")
    
    with connection.cursor() as cursor:
        try:
            # Obtener todas las tablas y sus columnas seriales (autoincrementales)
            cursor.execute("""
                SELECT 
                    t.relname as table_name,
                    s.relname as sequence_name,
                    a.attname as column_name
                FROM pg_class t
                JOIN pg_attribute a ON a.attrelid = t.oid
                JOIN pg_depend d ON d.refobjid = t.oid AND d.refobjsubid = a.attnum
                JOIN pg_class s ON s.oid = d.objid
                WHERE t.relkind = 'r' 
                AND s.relkind = 'S';
            """)
            
            sequences = cursor.fetchall()
            
            for table, sequence, column in sequences:
                print(f"Procesando tabla: {table}, secuencia: {sequence}")
                
                # Obtener el máximo ID actual
                cursor.execute(f'SELECT MAX("{column}") FROM "{table}";')
                res = cursor.fetchone()
                max_id = res[0] if res else 0
                
                if max_id is not None:
                    next_val = max_id + 1
                    print(f"  -> Max ID: {max_id}. Ajustando secuencia a: {next_val}")
                    cursor.execute(f'SELECT setval(\'{sequence}\', {next_val}, false);')
                else:
                    print(f"  -> Tabla vacía. No se requiere ajuste.")
                    
            print("Reparación completada exitosamente.")
            
        except Exception as e:
            print(f"Error durante la ejecución SQL: {e}")

if __name__ == '__main__':
    fix_sequences()
