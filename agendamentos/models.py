from django.db import models
from django.conf import settings

class Servico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    duracao_estimada = models.DurationField(null=True, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    especialidade = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, null=True, blank=True)
    data_horario = models.DateTimeField()
    status = models.CharField(max_length=20, default='agendado')  # ex: agendado, realizado, cancelado
    observacoes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data_horario']

    def __str__(self):
        return f'{self.servico} - {self.usuario} - {self.data_horario:%Y-%m-%d %H:%M}'
