from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Medicamento

@receiver(post_save, sender=Medicamento)
def diminuir_estoque(sender, instance, created, **kwargs):
    if created:  # Verifica se o medicamento está sendo criado (não atualizado)
        estoque = instance.estoque_medicamento
        estoque.quantidade -= 1  # Diminui a quantidade em 1
        estoque.save()