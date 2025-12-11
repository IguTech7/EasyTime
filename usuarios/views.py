from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('painel:dashboard')

    return render(request, 'usuarios/login.html')


def logout_usuario(request):
    logout(request)
    return redirect('usuarios:login')

def cadastro_usuario(request):
    return render(request, 'usuarios/cadastro.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Aqui você pode adicionar lógica para criar o usuário
        # Por simplicidade, vamos redirecionar para a página de login
        return redirect('usuarios:login')
