from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Funcionario(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'AT', 'Ativo'
        INATIVO = 'IN', 'Inativo'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=100)
    data_contratacao = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.ATIVO
    )
    
    def __str__(self):
        return self.nome