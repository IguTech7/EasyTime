from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'funcionario', 'data_horario', 'observacoes']
        widgets = {
            'data_horario': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
