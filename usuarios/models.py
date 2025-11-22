from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)  # mais pra frente podemos substituir por auth
    telefone = models.CharField(max_length=20, blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=50,
        choices=[
            ('cliente', 'Cliente'),
            ('admin', 'Administrador'),
            ('funcionario', 'Funcionário'),
        ],
        default='cliente'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
