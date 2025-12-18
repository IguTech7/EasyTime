from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPO_CHOICES = (
        ('cliente', 'Cliente'),
        ('profissional', 'Profissional'),
    )
    
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='cliente')
    
    def __str__(self):
        return self.username