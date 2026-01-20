from django import forms
from .models import Activo, Zona, Categoria, Marca, CentroCosto
from django.utils import timezone


class ImportarActivosForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Archivo Excel (.xlsx)',
        help_text='El archivo debe tener la misma estructura que el reporte exportado.'
    )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría',
                'id': 'id_nombre'
            }),
        }

class ActivoForm(forms.ModelForm):
    ESTADO_CHOICES_CREATE = [
        ('', ''),
        ('ACTIVO CONFIRMADO', 'Activo Confirmado'),
        ('ASIGNADO', 'Asignado'),
    ]
    
    ESTADO_CHOICES_UPDATE = [
        ('', ''),
        ('ACTIVO CONFIRMADO', 'Activo Confirmado'),
        ('ASIGNADO', 'Asignado'),
        ('DADO DE BAJA', 'Dado de Baja'),
    ]
    
    CARGO_CHOICES = [
        ('', ''),
        ('VENDEDOR AMBULANTE', 'Vendedor Ambulante'),
        ('RECAUDADOR', 'Recaudador'),
        ('VENDEDOR TAT', 'Vendedor TAT'),
        ('ADMINISTRATIVOS', 'Administrativos'),
    ]

    OPERADOR_CHOICES = [
        ('', ''),
        ('TIGO', 'Tigo'),
        ('MOVISTAR', 'Movistar'),
        ('CLARO', 'Claro'),
    ]

    class CentroCostoCodigoChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.codigo

    class CentroCostoNombreChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.nombre

    centro_costo_codigo_select = CentroCostoCodigoChoiceField(
        queryset=CentroCosto.objects.all(),
        label="Cód. Centro Costo",
        required=False,
        empty_label="",  # Empty string for Select2 placeholder compatibility
        widget=forms.Select(attrs={
            'class': 'form-select select2-basic', 
            'id': 'id_centro_costo_codigo_select',
            'data-placeholder': 'Seleccione un código'
        })
    )

    centro_costo_nombre_select = CentroCostoNombreChoiceField(
        queryset=CentroCosto.objects.all(),
        label="Nombre Centro Costo",
        required=False,
        empty_label="",  # Empty string for Select2 placeholder compatibility
        widget=forms.Select(attrs={
            'class': 'form-select select2-basic', 
            'id': 'id_centro_costo_nombre_select',
            'data-placeholder': 'Seleccione un nombre'
        })
    )
    
    class Meta:
        model = Activo
        exclude = ['fecha_confirmacion', 'fecha_creacion', 'fecha_modificacion', 'marca_old']
        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el documento',
                'list': 'documento-list'
            }),
            'nombres_apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombres y apellidos',
                'list': 'nombres-list'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'marca': forms.Select(attrs={'class': 'form-select select2-basic', 'id': 'id_marca', 'data-placeholder': 'Seleccione una marca'}),
            'zona': forms.Select(attrs={'class': 'form-select select2-basic', 'data-placeholder': 'Seleccione una zona'}),
            'cargo': forms.Select(attrs={'class': 'form-select select2-basic', 'data-placeholder': 'Seleccione un cargo'}),
            'estado': forms.Select(attrs={'class': 'form-select select2-basic', 'data-placeholder': 'Seleccione un estado'}),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identificación del responsable',
                'list': 'identificacion-list'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identificación del responsable',
                'list': 'identificacion-list'
            }),
            # 'codigo_centro_costo': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Código del centro de costo',
            #     'list': 'codigo-centro-list'
            # }),
            # 'centro_costo_punto': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Nombre del centro de costo',
            #     'list': 'nombre-centro-list'
            # }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese observaciones',
                'rows': 1,
                'style': 'overflow:hidden; resize:none;'
            }),
            'imei1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IMEI 1'}),
            'imei2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IMEI 2'}),
            'sn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'iccid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ICCID', 'id': 'id_iccid'}),
            'operador': forms.Select(attrs={'class': 'form-select select2-basic', 'id': 'id_operador', 'data-placeholder': 'Seleccione un operador'}),
            'mac_superflex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MAC Superflex'}),
            'activo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de activo'}),
            'punto_venta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Punto de venta'}),
            'fecha_salida_bodega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        is_assignment = kwargs.pop('is_assignment', False)
        super().__init__(*args, **kwargs)
        
        # Configurar choices para estado según si es creación o edición
        if is_update:
            self.fields['estado'].widget.choices = self.ESTADO_CHOICES_UPDATE
        else:
            self.fields['estado'].widget.choices = self.ESTADO_CHOICES_CREATE
            self.fields['estado'].initial = 'ACTIVO CONFIRMADO'
        
        # Configurar choices para cargo
        self.fields['cargo'].widget = forms.Select(attrs={'class': 'form-select select2-basic'})
        self.fields['cargo'].widget.choices = self.CARGO_CHOICES
        self.fields['cargo'].widget.choices = self.CARGO_CHOICES
        self.fields['cargo'].initial = 'VENDEDOR AMBULANTE'
        
        # Configurar choices para operador
        self.fields['operador'].widget.choices = self.OPERADOR_CHOICES
        
        # Configurar zona como select con las zonas existentes
        zonas = Zona.objects.all().values_list('nombre', 'nombre')
        self.fields['zona'].widget = forms.Select(attrs={'class': 'form-select select2-basic', 'data-placeholder': 'Seleccione una zona'})
        self.fields['zona'].widget.choices = [('', '')] + list(zonas)
        
        # Configurar categoría para que no muestre "----"
        self.fields['categoria'].empty_label = None
        
        # Configurar marca: si hay una categoría seleccionada, filtrar marcas
        if self.instance.pk and self.instance.categoria:
            # Si estamos editando y hay una categoría, filtrar marcas
            self.fields['marca'].queryset = Marca.objects.filter(categoria=self.instance.categoria)
        else:
            # Si estamos creando, mostrar todas las marcas (el filtrado se hará con JavaScript)
            self.fields['marca'].queryset = Marca.objects.all()
        
        # Configurar marca para que no muestre "----" si hay opciones
        # Configurar marca para que no muestre "----" si hay opciones
        if self.fields['marca'].queryset.exists():
            self.fields['marca'].empty_label = "" # Empty string for Select2 placeholder

        if self.instance.pk and self.instance.codigo_centro_costo:
            try:
                cc = CentroCosto.objects.filter(codigo=self.instance.codigo_centro_costo).first()
                if cc:
                    self.fields['centro_costo_codigo_select'].initial = cc
                    self.fields['centro_costo_nombre_select'].initial = cc
            except Exception:
                pass
        
        # Hacer obligatorios todos los campos de la sección "Datos del Activo"
        # Hacer obligatorios todos los campos de la sección "Datos del Activo" y asignación inicial
        campos_obligatorios = [
            'categoria', 'marca', 'activo', 'sn', 
            'imei1', 'imei2', 'estado', 'zona',
            'responsable', 'identificacion', 
            'centro_costo_codigo_select', 'centro_costo_nombre_select'
        ]
        
        for campo in campos_obligatorios:
            if campo in self.fields:
                self.fields[campo].required = True

        # Lógica para asignación: bloquear campos fundamentales (identidad del activo)
        # pero permitir editar campos de asignación (usuario, ubicación, etc.) incluso si ya tienen valor
        if is_assignment and self.instance.pk:
            # Campos obligatorios para asignación según requerimiento
            campos_obligatorios_asignacion = [
                'cargo', 'nombres_apellidos', 
                'centro_costo_codigo_select', 'centro_costo_nombre_select', 
                'punto_venta', 'iccid', 'operador'
            ]
            for campo in campos_obligatorios_asignacion:
                if campo in self.fields:
                    self.fields[campo].required = True

            # Campos que siempre deben ser editables durante una asignación/reasignación
            assignment_fields = [
                'documento', 'nombres_apellidos', 'responsable', 'identificacion',
                'zona', 'cargo', 
                'centro_costo_codigo_select', 'centro_costo_nombre_select',
                'punto_venta', 'observacion', 'estado', 'iccid', 'operador'
            ]
            
            # Asegurar que los campos obligatorios también estén en assignment_fields para que sean editables
            # (ya están la mayoría, agregamos operador/iccid arriba a assignment_fields explícitamente)

            for name, field in self.fields.items():
                # Si el campo es de asignación, saltar bloqueo (permitir edición)
                if name in assignment_fields:
                    continue

                # Obtener valor del campo en la instancia
                value = getattr(self.instance, name, None)
                
                # Si el campo tiene valor (no es None ni string vacío), hacerlo readonly
                if value and value != '':
                    # Para campos de texto/input
                    field.widget.attrs['readonly'] = 'readonly'
                    field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' bg-light'
                    
                    # Para selects, readonly no funciona igual en HTML, se usa disabled
                    # pero disabled no envía el valor en el POST, así que necesitamos simularlo
                    if isinstance(field.widget, forms.Select):
                        field.widget.attrs['style'] = 'pointer-events: none; background-color: #e9ecef;'
                        field.widget.attrs['tabindex'] = '-1'
                        field.widget.attrs['aria-disabled'] = 'true'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Actualizar campos de texto desde el select de Centro de Costo (usamos cualquiera de los dos)
        cc = self.cleaned_data.get('centro_costo_codigo_select')
        if not cc:
            cc = self.cleaned_data.get('centro_costo_nombre_select')
            
        if cc:
            instance.codigo_centro_costo = cc.codigo
            instance.centro_costo_punto = cc.nombre
        
        # Establecer fecha_confirmacion si es un nuevo activo
        if not instance.pk:
            instance.fecha_confirmacion = timezone.now().date()
        
        # Actualizar estado basado en documento y nombres
        if instance.documento and instance.nombres_apellidos:
            if instance.estado == 'ACTIVO CONFIRMADO':
                instance.estado = 'ASIGNADO'
        
        if commit:
            instance.save()
        return instance
