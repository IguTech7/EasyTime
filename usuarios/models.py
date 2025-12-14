# usuarios/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Tipos de usuário definidos
    TIPO_CHOICES = (
        ('cliente', 'Cliente'),
        ('funcionario', 'Funcionário'),
        ('administrador', 'Administrador'),
    )
    
    # Adiciona o campo 'tipo'
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='cliente')

    # Você pode adicionar outros campos específicos aqui

    def __str__(self):
        return self.username