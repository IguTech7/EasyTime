from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    especialidade = models.CharField(max_length=100)
    data_contratacao = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
        ],
        default='ativo'
    )

    def __str__(self):
        return self.nome