from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email") 
    
    OPCOES_CADASTRO = [
        ('cliente', 'Cliente'),
        ('profissional', 'Profissional'),
    ]
    
    tipo = forms.ChoiceField(
        choices=OPCOES_CADASTRO,
        label="Eu sou",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
            
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Nome de Usuário'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Email'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Senha'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Confirmação de Senha'