from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Activo

@login_required
def home(request):
    activos = Activo.objects.all()
    return render(request, 'activos/home.html', {'activos': activos})

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

