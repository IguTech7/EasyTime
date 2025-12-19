from django import forms
from django.contrib.auth import get_user_model
from .models import Funcionario

User = get_user_model()

class FuncionarioForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=True,
        label="Usuário",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Funcionario
        fields = ['user', 'telefone', 'foto']