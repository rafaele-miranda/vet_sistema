from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DadosAnimal, Medicamento, Procedimento, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DadosAnimal)
admin.site.register(Medicamento)
admin.site.register(Procedimento)

