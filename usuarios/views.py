from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from .forms import CustomAuthenticationForm, CustomUserCreationForm

class LoginView(BaseLoginView):
    template_name = 'usuarios/login.html'
    authentication_form = CustomAuthenticationForm

def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados fornecidos.')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'usuarios/cadastro.html', context)