from django import forms
from agendamentos.models import Agendamento, Servico, Funcionario
from django.contrib.auth import get_user_model
from django.forms import Select

User = get_user_model()

class AgendamentoForm(forms.ModelForm):
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.all(),
        empty_label="Selecione um Serviço",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Serviço Desejado"
    )

    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(), 
        empty_label="Selecione um Profissional",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Profissional"
    )

    data_agendamento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Clique para selecionar a data',
            'type': 'date'
        }),
        label="Data"
    )

    hora_agendamento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 14:30',
            'type': 'time'
        }),
        label="Hora"
    )

    class Meta:
        model = Agendamento
        fields = ['servico', 'funcionario', 'data_agendamento', 'hora_agendamento']
        
        widgets = {
            'servico': Select(attrs={'class': 'form-select'}),
            'funcionario': Select(attrs={'class': 'form-select'}),
        }