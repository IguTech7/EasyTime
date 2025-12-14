from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Servico
from .forms import ServicoForm

def is_funcionario_or_staff(user):
    return user.is_staff or user.tipo == 'funcionario'

@login_required
@user_passes_test(is_funcionario_or_staff)
def listar_servicos(request):
    servicos = Servico.objects.all().order_by('nome')
    context = {'servicos': servicos}
    return render(request, 'servicos/listar_servicos.html', context)

@login_required
@user_passes_test(is_funcionario_or_staff)
def criar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('servicos:listar')
    else:
        form = ServicoForm()
        
    context = {'form': form, 'titulo': 'Criar Novo Serviço'}
    return render(request, 'servicos/form_servico.html', context)

@login_required
@user_passes_test(is_funcionario_or_staff)
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, f'Serviço "{servico.nome}" atualizado com sucesso!')
            return redirect('servicos:listar')
    else:
        form = ServicoForm(instance=servico)
        
    context = {'form': form, 'titulo': f'Editar Serviço: {servico.nome}'}
    return render(request, 'servicos/form_servico.html', context)

@login_required
@user_passes_test(is_funcionario_or_staff)
def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        servico.delete()
        messages.success(request, f'Serviço "{servico.nome}" excluído com sucesso!')
        return redirect('servicos:listar')
        
    messages.error(request, 'A exclusão deve ser feita via POST.')
    return redirect('servicos:listar')