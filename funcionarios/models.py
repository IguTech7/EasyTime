from django.db import models
from django.conf import settings
from servicos.models import Servico 

class Funcionario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil_funcionario'
    )
    
    especialidades = models.ManyToManyField(
        Servico, 
        blank=True, 
        related_name='funcionarios_especialistas'
    )
    
    telefone = models.CharField(max_length=21, blank=True, null=True)
    foto = models.ImageField(upload_to='funcionarios/', blank=True, null=True)

    def __str__(self):
        return self.user.username