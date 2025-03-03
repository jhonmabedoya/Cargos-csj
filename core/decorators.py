from django.core.exceptions import PermissionDenied
from functools import wraps

def requiere_magistrado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo_usuario != 'MAG':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper 