from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def rol_requerido(roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'perfil'):
                if request.user.perfil.rol in roles_permitidos:
                    return view_func(request, *args, **kwargs)
            return redirect('no_autorizado')
        return wrapper
    return decorador
