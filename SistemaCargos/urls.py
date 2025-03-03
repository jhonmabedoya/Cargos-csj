from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cargos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('despachos/crear/', views.crear_despacho, name='crear_despacho'),
    path('despachos/', views.listar_despachos, name='despachos'),
    path('despachos/exportar/', views.exportar_despachos, name='exportar_despachos'),
    path('novedades/', views.listar_novedades, name='novedades'),
    path('funcionarios/', views.listar_funcionarios, name='funcionarios'),
    path('crear_funcionario/', views.crear_funcionario, name='crear_funcionario'),
    path('despachos/<int:pk>/editar/', views.editar_despacho, name='editar_despacho'),
    path('despachos/<int:pk>/eliminar/', views.eliminar_despacho, name='eliminar_despacho'),
]
