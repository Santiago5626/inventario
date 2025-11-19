from django.urls import path
from . import views

app_name = 'activos'

urlpatterns = [
    path('', views.home, name='home'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('crear/', views.ActivoCreateView.as_view(), name='crear_activo'),
    path('<int:pk>/', views.ActivoDetailView.as_view(), name='detalle_activo'),
    path('<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='editar_activo'),
    path('<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='eliminar_activo'),
]
