import os
import sys
import django

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_pda.settings')
django.setup()

from activos.forms import ActivoForm
from activos.models import Activo, CentroCosto, Categoria, Marca, Zona

import traceback

def verify_form():
    try:
        print("Verifying ActivoForm logic...")
        
        # Ensure we have a CentroCosto
        cc = CentroCosto.objects.filter(codigo="6972").first()
        if not cc:
            print("ERROR: CentroCosto 6972 not found. Migration might have failed.")
            return

        print(f"Found CentroCosto: {cc}")

        # Ensure dependencies exist
        zona, _ = Zona.objects.get_or_create(nombre="TestZona")
        categoria, _ = Categoria.objects.get_or_create(nombre="TestCat")
        marca, _ = Marca.objects.get_or_create(nombre="TestMarca", categoria=categoria)

        # Test 1: Create Activo using form and centro_costo_select
        print("\nTest 1: Create Activo with centro_costo_select")
        data = {
            'activo': 'Test Activo 1',
            'marca': marca.id,
            'categoria': categoria.id,
            'zona': zona.id, # Zona is a Model or CharField?
            'estado': 'activo confirmado',
            'sn': 'SN123',
            'imei1': 'IMEI1',
            'imei2': 'IMEI2',
            'responsable': 'Test User',
            'identificacion': '12345',
            'centro_costo_select': cc.id,
        }
        
        # Check Zona model definition
        # class Zona(models.Model): ...
        # class Activo(models.Model):
        #     zona = models.CharField(max_length=100, default="Valledupar", verbose_name="ZONA")
        
        # Wait! Activo.zona is a CharField, NOT a ForeignKey!
        # But ActivoForm defines it as a Select with choices from Zona model.
        # "self.fields['zona'].widget.choices = [('', '')] + list(zonas)"
        # where zonas = Zona.objects.all().values_list('nombre', 'nombre')
        # So it expects a STRING name, not an ID.
        
        data['zona'] = zona.nombre
        
        form = ActivoForm(data=data)
        if form.is_valid():
            instance = form.save()
            print(f"Activo created: {instance.codigo_centro_costo} - {instance.centro_costo_punto}")
            if instance.codigo_centro_costo == cc.codigo and instance.centro_costo_punto == cc.nombre:
                print("SUCCESS: Activo fields updated correctly from selection.")
            else:
                print("FAILURE: Activo fields NOT updated correctly.")
        else:
            print("FAILURE: Form is invalid")
            print(form.errors)

        # Test 2: Initialize form with existing Activo
        print("\nTest 2: Initialize form with existing Activo")
        # Manually set fields to match a CC
        instance.codigo_centro_costo = "6972"
        instance.save()
        
        form_edit = ActivoForm(instance=instance)
        initial_cc = form_edit.fields['centro_costo_select'].initial
        print(f"Initial CentroCosto: {initial_cc}")
        
        if initial_cc == cc:
            print("SUCCESS: Form initialized with correct CentroCosto.")
        else:
            print("FAILURE: Form NOT initialized with correct CentroCosto.")
            
        # Clean up test data
        instance.delete()

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    verify_form()
