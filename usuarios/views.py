from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import requiere_admin_o_magistrado, requiere_admin, requiere_magistrado
from .models import Usuario
from .forms import UsuarioForm, CambiarPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
@requiere_admin
def lista(request):
    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count()
    })

@login_required
@requiere_admin
def crear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:lista')
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Crear Usuario'
    })

@login_required
@requiere_admin
def editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:lista')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Editar Usuario',
        'usuario': usuario
    })

@login_required
@requiere_admin
def eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    # Evitar que se elimine a sí mismo
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('usuarios:lista')
    
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/confirmar_eliminar.html', {
        'objeto': usuario,
        'titulo': 'Eliminar Usuario'
    })

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Por favor corrige los errores indicados.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_password.html', {
        'form': form
    })

@login_required
def perfil(request):
    """Vista para mostrar y editar el perfil del usuario."""
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    }) 