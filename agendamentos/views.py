from django.shortcuts import render, redirect
from .models import Agendamento
from .forms import AgendamentoForm
from django.contrib.auth.decorators import login_required

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user)
    return render(request, 'agendamentos/listar.html', {'agendamentos': agendamentos})

@login_required
def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            agendamento.save()
            return redirect('agendamentos:listar')
    else:
        form = AgendamentoForm()

    return render(request, 'agendamentos/criar.html', {'form': form})
