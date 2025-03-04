from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
] 