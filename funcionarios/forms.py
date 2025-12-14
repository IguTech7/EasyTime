from django import forms
from funcionarios.models import Funcionario
from django.contrib.auth import get_user_model

User = get_user_model()

class FuncionarioForm(forms.ModelForm):
    
    # Campo para selecionar o usuário (CustomUser)
    # É importante listar apenas usuários que ainda não são funcionários
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(tipo='funcionario', funcionario__isnull=True),
        empty_label="Selecione o Usuário",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Usuário Associado"
    )

    class Meta:
        model = Funcionario
        # REMOVEMOS 'data_contratacao' daqui.
        fields = ['user', 'nome', 'email', 'telefone', 'especialidade', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }