from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PerfilForm
from django.core.exceptions import PermissionDenied

from .models import Perfil
from django.shortcuts import get_object_or_404, render

@login_required
def ver_perfil(request, username=None):
    if username is None:
        perfil = request.user.perfil
    else:
        perfil = get_object_or_404(Perfil, user__username=username)

        if perfil.user != request.user:
            raise PermissionDenied("Você não tem permissão para acessar este perfil.")

    return render(request, 'perfil.html', {'perfil': perfil})

@login_required
def editar_perfil(request, username=None):
    if username is None:
        perfil = request.user.perfil
    else:
        perfil = get_object_or_404(Perfil, user__username=username)

        if perfil.user != request.user:
            raise PermissionDenied("Você não tem permissão para acessar este perfil.")

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('read')  
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'editar_perfil.html', {'form': form})

