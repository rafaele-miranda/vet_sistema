from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def grupo_colaborador_required(groups):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                raise PermissionDenied("Você não tem permissão para acessar esta página.")
                return redirect('home')
        return wrapper
    return decorator