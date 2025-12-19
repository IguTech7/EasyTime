from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
from funcionarios.models import Funcionario
from servicos.models import Servico
from django.utils import timezone
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from servicos.models import Servico
from funcionarios.models import Funcionario

@login_required
def dashboard(request):
    user = request.user
    hoje = timezone.now().date()
    
    data_get = request.GET.get('data')
    
    if data_get:
        try:
            data_selecionada = datetime.strptime(data_get, '%Y-%m-%d').date()
        except ValueError:
            data_selecionada = hoje
    else:
        data_selecionada = hoje

    if user.tipo == 'cliente':
        agendamentos = Agendamento.objects.filter(usuario=user).order_by('data_horario')
        template = 'painel/dashboard_cliente.html'
    else:
        agendamentos = Agendamento.objects.filter(
            funcionario__user=user, 
            data_horario__date=data_selecionada
        ).order_by('data_horario')
        template = 'painel/dashboard_funcionario.html'

    context = {
        'agendamentos': agendamentos,
        'total_futuros': agendamentos.count(),
        'servicos_disponiveis': Servico.objects.all(),
        'perfil_funcionario': getattr(user, 'funcionario', None),
        'data_hoje': hoje,
        'data_selecionada': data_selecionada,
    }
    return render(request, template, context)

@login_required
def atualizar_perfil_profissional(request):
    if request.method == 'POST':
        perfil = get_object_or_404(Funcionario, user=request.user)
        
        servicos_escolhidos = request.POST.getlist('especialidades')
        
        perfil.especialidades.set(servicos_escolhidos)
        
        messages.success(request, "Perfil e especialidades atualizados com sucesso!")
        return redirect('painel:dashboard')
    
    return redirect('painel:dashboard')

@login_required
def atualizar_especialidades(request):
    if request.method == 'POST':
        perfil = get_object_or_404(Funcionario, user=request.user)
        
        servicos_ids = request.POST.getlist('especialidades')
        
        perfil.especialidades.set(servicos_ids)
        
        messages.success(request, "Suas especialidades foram atualizadas!")
    
    return redirect('painel:dashboard')