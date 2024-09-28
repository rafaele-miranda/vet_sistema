from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from perfil.models import Perfil

class Command(BaseCommand):
    help = 'Cria perfis para todos os usuários existentes'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'perfil'):
                Perfil.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Perfil criado para o usuário: {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Perfil já existe para o usuário: {user.username}'))
