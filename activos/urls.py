from django.urls import path
from . import views

app_name = 'activos'

urlpatterns = [
    path('', views.ActivoListView.as_view(), name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logistica-dashboard/', views.logistica_dashboard, name='logistica_dashboard'),
    path('lectura-dashboard/', views.lectura_dashboard, name='lectura_dashboard'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('reporte-por-sede/', views.reporte_por_sede, name='reporte_por_sede'),
    path('activos/crear/', views.ActivoCreateView.as_view(), name='activo-create'),
    path('activos/<int:pk>/', views.ActivoDetailView.as_view(), name='activo_detail'),
    path('activos/<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='activo_update'),
    path('activos/<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='activo_delete'),
    path('activos/<int:pk>/historial/', views.historial_activo, name='historial_activo'),
    path('activos/<int:pk>/movimiento/', views.RegistrarMovimientoView.as_view(), name='registrar-movimiento'),

    path('movimientos/', views.MovimientoListView.as_view(), name='movimientos'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Articulos
    path('articulos/', views.ArticuloListView.as_view(), name='articulo_list'),
    path('articulos/crear/', views.ArticuloCreateView.as_view(), name='articulo_create'),
    path('articulos/<int:pk>/editar/', views.ArticuloUpdateView.as_view(), name='articulo_update'),
    path('articulos/<int:pk>/eliminar/', views.ArticuloDeleteView.as_view(), name='articulo_delete'),

    # Zonas
    path('zonas/', views.ZonaListView.as_view(), name='zona_list'),
    path('zonas/crear/', views.ZonaCreateView.as_view(), name='zona_create'),
    path('zonas/<int:pk>/editar/', views.ZonaUpdateView.as_view(), name='zona_update'),
    path('zonas/<int:pk>/eliminar/', views.ZonaDeleteView.as_view(), name='zona_delete'),
]
