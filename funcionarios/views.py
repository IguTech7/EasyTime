from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import FuncionarioForm
from .models import Funcionario

def is_staff(user):
    return user.is_staff

@login_required(login_url='usuarios:login')
@user_passes_test(is_staff, login_url='/painel/')
def criar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.status = 'AT'
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('funcionarios:listar')
        else:
            messages.error(request, 'Erro no formulário. Verifique os campos.')
    else:
        form = FuncionarioForm()
        
    context = {
        'form': form,
        'titulo': 'Cadastrar Novo Funcionário',
        'botao_submit': 'Cadastrar'
    }
    return render(request, 'funcionarios/criar_funcionario.html', context)

@login_required(login_url='usuarios:login')
@user_passes_test(is_staff, login_url='/painel/')
def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all().order_by('nome')
    context = {
        'funcionarios': funcionarios,
        'titulo': 'Gerenciar Funcionários'
    }
    return render(request, 'funcionarios/listar_funcionarios.html', context)

@login_required(login_url='usuarios:login')
@user_passes_test(is_staff, login_url='/painel/')
def detalhar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    context = {
        'funcionario': funcionario,
        'titulo': f'Detalhes de {funcionario.nome}'
    }
    return render(request, 'funcionarios/detalhar_funcionario.html', context)

@login_required(login_url='usuarios:login')
@user_passes_test(is_staff, login_url='/painel/')
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Funcionário {funcionario.nome} atualizado com sucesso.')
            return redirect('funcionarios:listar')
        else:
            messages.error(request, 'Erro ao atualizar o funcionário. Verifique os campos.')
    else:
        form = FuncionarioForm(instance=funcionario)
        
    context = {
        'form': form,
        'titulo': f'Editar Funcionário: {funcionario.nome}',
        'botao_submit': 'Salvar Alterações'
    }
    return render(request, 'funcionarios/criar_funcionario.html', context)

@login_required(login_url='usuarios:login')
@user_passes_test(is_staff, login_url='/painel/')
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        nome = funcionario.nome
        funcionario.delete()
        
        messages.success(request, f'Funcionário {nome} excluído permanentemente.')
        return redirect('funcionarios:listar')
        
    return render(request, 'funcionarios/confirmar_exclusao.html', {'funcionario': funcionario})