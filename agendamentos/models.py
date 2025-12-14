from django.db import models
from django.conf import settings
from servicos.models import Servico
from funcionarios.models import Funcionario

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AG', 'Agendado'),
        ('PE', 'Pendente'),
        ('CA', 'Cancelado'),
        ('RE', 'Realizado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos', null=True)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, null=True, blank=True)
    data_horario = models.DateTimeField()
    
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE'
    )
    observacoes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_horario']

    def __str__(self):
        return f'{self.servico} - {self.usuario} - {self.data_horario:%Y-%m-%d %H:%M}'