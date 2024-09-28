from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path



urlpatterns = [
    path('perfil/', views.ver_perfil, name='perfil'),
    path('editar/<str:username>/', views.editar_perfil, name='editar_perfil'),

    
]

