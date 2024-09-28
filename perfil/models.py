from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 


class Perfil(models.Model):   
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='perfil') 
    foto = models.ImageField(upload_to='perfil/foto/', blank=True)  
    ocupacao = models.CharField(max_length=120, blank=True, verbose_name='Ocupação')
    descricao = models.TextField(blank=True, verbose_name='Descrição')  
    genero = models.CharField(max_length=20, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, blank=True) 

    def __str__(self):
         return f'{self.user.username} Profile'

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
