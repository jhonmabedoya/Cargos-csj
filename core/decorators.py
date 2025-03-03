from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def requiere_magistrado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.tipo_usuario == 'magistrado':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('core:dashboard')
    return wrapper

def requiere_admin_o_magistrado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.tipo_usuario == 'magistrado':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('core:dashboard')
    return wrapper 