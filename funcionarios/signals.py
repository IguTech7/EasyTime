from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from .models import Funcionario

CustomUser = settings.AUTH_USER_MODEL

@receiver(post_save, sender=CustomUser)
def create_funcionario_profile(sender, instance, created, **kwargs):
    
    if created and instance.tipo == 'funcionario':
        Funcionario.objects.create(
            user=instance,
            nome=instance.username,
            email=instance.email,
            data_contratacao=timezone.now().date() 
        )