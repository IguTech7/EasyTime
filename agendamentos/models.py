from django.db import models
from usuarios.models import Usuario
from funcionarios.models import Funcionario
from servicos.models import Servico

class Agendamento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True)

    data_horario = models.DateTimeField()
    observacoes = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('cancelado', 'Cancelado'),
            ('concluido', 'Concluído'),
        ],
        default='pendente'
    )

    def __str__(self):
        return f"{self.usuario.nome} - {self.servico.nome} ({self.data_horario})"