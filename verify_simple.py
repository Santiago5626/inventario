import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_pda.settings')
django.setup()

from activos.forms import ActivoForm
from activos.models import Activo, CentroCosto, Categoria, Marca, Zona

def run():
    print("--- START DEBUG ---")
    try:
        # Get data
        cc = CentroCosto.objects.first()
        if not cc:
            print("No CentroCosto found!")
            return
        print(f"Using CentroCosto: {cc.pk} - {cc.codigo} - {cc.nombre}")

        # Ensure related data
        zona_name = "Valledupar" 
        # Ensure Zona 'Valledupar' exists in Zona table if referenced by choices?
        # Form choices come from Zona model!
        z, created = Zona.objects.get_or_create(nombre=zona_name)
        print(f"Zona: {z.nombre}")

        cat, _ = Categoria.objects.get_or_create(nombre="Tecnologia")
        marca, _ = Marca.objects.get_or_create(nombre="Samsung", categoria=cat)
        
        data = {
            'activo': 'Test Activo Debug',
            'marca': marca.id,
            'categoria': cat.id,
            'zona': zona_name, # Value matches choice key
            'estado': 'activo confirmado',
            'sn': 'SN_DEBUG',
            'imei1': 'IMEI1_DEBUG',
            'imei2': 'IMEI2_DEBUG',
            'responsable': 'Debug User',
            'identificacion': '99999',
            'observacion': 'Test Observacion',
            'centro_costo_codigo_select': cc.id,
            'centro_costo_nombre_select': cc.id,
        }
        
        print("Initializing Form...")
        form = ActivoForm(data=data)
        
        print("Validating Form...")
        if form.is_valid():
            print("Form is VALID.")
            instance = form.save()
            print(f"Saved Instance: ID={instance.item}, CC_CODE={instance.codigo_centro_costo}, CC_PUNTO={instance.centro_costo_punto}")
            
            if instance.codigo_centro_costo == cc.codigo and instance.centro_costo_punto == cc.nombre:
                print("VERIFICATION SUCCESSFUL")
            else:
                print("VERIFICATION FAILED: Fields mismatch")
        else:
            print("Form is INVALID.")
            print(form.errors.as_text())
            
    except Exception as e:
        print("EXCEPTION OCCURRED:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run()
