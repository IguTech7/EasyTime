from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from agendamentos.models import Agendamento, Servico, Funcionario
from datetime import date, datetime, time

def home(request):
    if request.user.is_authenticated:
        return redirect('painel:dashboard')
    return render(request, 'painel/home_page.html')

@never_cache
@login_required(login_url='usuarios:login')
def dashboard(request):
    context = {}
    hoje = date.today()
    
    if request.user.tipo == 'cliente':
        total_futuros = Agendamento.objects.filter(
            usuario=request.user, 
            data_horario__date__gte=hoje
        ).exclude(status='CA').count()

        proximos_agendamentos = Agendamento.objects.filter(
            usuario=request.user, 
            data_horario__date__gte=hoje
        ).exclude(status='CA').order_by('data_horario')

        servicos_disponiveis = Servico.objects.all()

        context.update({
            'total_futuros': total_futuros,
            'proximo_agendamento': proximos_agendamentos.first(), 
            'proximos_agendamentos': proximos_agendamentos[:3],
            'servicos_disponiveis': servicos_disponiveis,
        })
        
    elif request.user.tipo == 'funcionario' or request.user.is_staff:
        
        inicio_do_dia = datetime.combine(hoje, time.min)
        fim_do_dia = datetime.combine(hoje, time.max)
        
        agendamentos_hoje = Agendamento.objects.filter(
            data_horario__range=(inicio_do_dia, fim_do_dia)
        ).exclude(status='CA').order_by('data_horario')
        
        if request.user.tipo == 'funcionario' and not request.user.is_staff:
            try:
                perfil_funcionario = Funcionario.objects.get(user=request.user)
                agendamentos_hoje = agendamentos_hoje.filter(funcionario=perfil_funcionario)
            except Funcionario.DoesNotExist:
                agendamentos_hoje = Agendamento.objects.none()
        
        context.update({
            'agendamentos_hoje_count': agendamentos_hoje.count(),
            'agendamentos_hoje_list': agendamentos_hoje,
        })

    return render(request, 'painel/dashboard.html', context)