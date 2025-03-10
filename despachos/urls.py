from django.urls import path
from . import views

app_name = 'despachos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('exportar/', views.exportar, name='exportar'),
] 