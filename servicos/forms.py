from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'step': '5'}),
        }
        labels = {
            'nome': 'Nome do Serviço',
            'descricao': 'Descrição Detalhada',
            'preco': 'Preço (R$)',
            'duracao': 'Duração (minutos)',
        }