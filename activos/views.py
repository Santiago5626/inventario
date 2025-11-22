from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from django.contrib.auth.models import Group
from django.db import models
from django.contrib import messages
from .models import Activo, Movimiento, Historial, Articulo

@login_required
def dashboard_redirect(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'Admin' in user_groups:
        return redirect(reverse('activos:admin_dashboard'))
    elif 'Logística' in user_groups:
        return redirect(reverse('activos:logistica_dashboard'))
    elif 'Lectura' in user_groups:
        return redirect(reverse('activos:lectura_dashboard'))
    else:
        return redirect(reverse('activos:home'))

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('activos:home')
    total_activos = Activo.objects.count()
    asignados = Activo.objects.filter(estado__icontains='asignado').count()
    en_bodega = Activo.objects.filter(estado__icontains='bodega').count()
    dados_baja = Activo.objects.filter(estado__icontains='baja').count()
    return render(request, 'activos/admin_dashboard.html', {
        'total_activos': total_activos,
        'asignados': asignados,
        'en_bodega': en_bodega,
        'dados_baja': dados_baja,
    })

@login_required
def logistica_dashboard(request):
    if not request.user.groups.filter(name='Logística').exists():
        return redirect('activos:home')
    activos_por_estado = Activo.objects.values('estado').annotate(count=models.Count('estado'))
    movimientos_recientes = Movimiento.objects.order_by('-fecha')[:10]
    return render(request, 'activos/logistica_dashboard.html', {
        'activos_por_estado': activos_por_estado,
        'movimientos_recientes': movimientos_recientes,
    })

@login_required
def lectura_dashboard(request):
    if not request.user.groups.filter(name='Lectura').exists():
        return redirect('activos:home')
    total_activos = Activo.objects.count()
    return render(request, 'activos/lectura_dashboard.html', {
        'total_activos': total_activos,
    })

class ActivoListView(LoginRequiredMixin, ListView):
    model = Activo
    template_name = 'activos/home.html'
    context_object_name = 'activos'


@login_required
def exportar_excel(request):
    activos = Activo.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario de Activos"

    # Headers
    headers = [field.name for field in Activo._meta.get_fields()]
    ws.append(headers)

    # Data
    for activo in activos:
        row = []
        for field in headers:
            row.append(str(getattr(activo, field)))
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventario_activos.xlsx'
    wb.save(response)
    return response

class ActivoCreateView(LoginRequiredMixin, CreateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

class ActivoDetailView(LoginRequiredMixin, DetailView):
    model = Activo
    template_name = 'activos/activo_detail.html'

class ActivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

class ActivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Activo
    template_name = 'activos/activo_confirm_delete.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)





# Movimiento CRUD
class MovimientoListView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'activos/movimiento_list.html'
    context_object_name = 'movimientos'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para ver movimientos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Movimiento registration
class RegistrarMovimientoView(LoginRequiredMixin, CreateView):
    model = Movimiento
    fields = ['tipo', 'zona_origen', 'zona_destino', 'estado_nuevo', 'descripcion']
    template_name = 'activos/registrar_movimiento.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para registrar movimientos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activo'] = get_object_or_404(Activo, pk=self.kwargs['pk'])
        # Obtener zonas únicas de los activos
        context['zonas'] = Activo.objects.values_list('zona', flat=True).distinct()
        return context

    def form_valid(self, form):
        activo = get_object_or_404(Activo, pk=self.kwargs['pk'])
        form.instance.activo = activo
        form.instance.usuario = self.request.user
        form.instance.estado_anterior = activo.estado

        if form.cleaned_data['estado_nuevo']:
            activo.estado = form.cleaned_data['estado_nuevo']
            activo.save()

        if form.cleaned_data['zona_destino']:
            activo.zona = form.cleaned_data['zona_destino']
            activo.save()

        messages.success(self.request, 'Movimiento registrado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('activos:activo_detail', kwargs={'pk': self.kwargs['pk']})


# Historial de activo
@login_required
def historial_activo(request, pk):
    activo = get_object_or_404(Activo, pk=pk)
    historial = Historial.objects.filter(activo=activo).order_by('-fecha')
    movimientos = Movimiento.objects.filter(activo=activo).order_by('-fecha')
    return render(request, 'activos/historial_activo.html', {
        'activo': activo,
        'historial': historial,
        'movimientos': movimientos,
    })

# Reporte por sede
@login_required
def reporte_por_sede(request):
    if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
        messages.error(request, 'No tienes permisos para ver reportes.')
        return redirect('activos:home')

    zona_nombre = request.GET.get('zona')
    if zona_nombre:
        activos = Activo.objects.filter(zona=zona_nombre)
    else:
        activos = Activo.objects.all()
        zona_nombre = None

    zonas = Activo.objects.values_list('zona', flat=True).distinct()
    return render(request, 'activos/reporte_por_zona.html', {
        'activos': activos,
        'zonas': zonas,
        'zona_seleccionada': zona_nombre,
    })

@login_required
def exportar_csv(request):
    activos = Activo.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=inventario_activos.csv'
    writer = csv.writer(response)
    writer.writerow([field.name for field in Activo._meta.get_fields()])
    for activo in activos:
        writer.writerow([str(getattr(activo, field.name)) for field in Activo._meta.get_fields()])
    return response

# Update ActivoUpdateView for permissions
class ActivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para editar activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Update ActivoCreateView for permissions
class ActivoCreateView(LoginRequiredMixin, CreateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)


# Articulo CRUD
class ArticuloListView(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = 'activos/articulo_list.html'
    context_object_name = 'articulos'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver artículos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ArticuloCreateView(LoginRequiredMixin, CreateView):
    model = Articulo
    fields = '__all__'
    template_name = 'activos/articulo_form.html'
    success_url = reverse_lazy('activos:articulo_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear artículos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ArticuloUpdateView(LoginRequiredMixin, UpdateView):
    model = Articulo
    fields = '__all__'
    template_name = 'activos/articulo_form.html'
    success_url = reverse_lazy('activos:articulo_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar artículos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ArticuloDeleteView(LoginRequiredMixin, DeleteView):
    model = Articulo
    template_name = 'activos/articulo_confirm_delete.html'
    success_url = reverse_lazy('activos:articulo_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar artículos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)


# Zona CRUD
from .models import Zona

class ZonaListView(LoginRequiredMixin, ListView):
    model = Zona
    template_name = 'activos/zona_list.html'
    context_object_name = 'zonas'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaCreateView(LoginRequiredMixin, CreateView):
    model = Zona
    fields = '__all__'
    template_name = 'activos/zona_form.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Zona
    fields = '__all__'
    template_name = 'activos/zona_form.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Zona
    template_name = 'activos/zona_confirm_delete.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

