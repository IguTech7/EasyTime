from django.shortcuts import render, redirect
from .models import Servico
from .forms import ServicoForm
from django.contrib.auth.decorators import login_required


@login_required
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos/listar.html', {'servicos': servicos})


@login_required
def criar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicos:listar')
    else:
        form = ServicoForm()

    return render(request, 'servicos/criar.html', {'form': form})
