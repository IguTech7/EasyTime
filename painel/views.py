from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
from funcionarios.models import Funcionario
from servicos.models import Servico
from django.utils import timezone
from datetime import date

@login_required
def dashboard(request):
    # Pega a data e hora atual do servidor local (Brasil)
    agora = timezone.localtime(timezone.now())
    hoje = agora.date()
    context = {}

    # --- LÓGICA PARA CLIENTE ---
    if request.user.tipo == 'cliente':
        # Busca agendamentos do cliente logado que NÃO foram cancelados
        agendamentos_cliente = Agendamento.objects.filter(
            usuario=request.user
        ).exclude(status='CA')

        # Filtra apenas agendamentos de hoje para o futuro
        futuros = agendamentos_cliente.filter(data_horario__date__gte=hoje)
        
        # Variáveis que o seu HTML utiliza
        context['total_futuros'] = futuros.count()
        context['proximo_agendamento'] = futuros.order_by('data_horario').first()
        context['proximos_agendamentos'] = futuros.order_by('data_horario') # Para a lista lá de baixo
        context['servicos_disponiveis'] = Servico.objects.all()

    # --- LÓGICA PARA PROFISSIONAL / FUNCIONÁRIO / STAFF ---
    elif request.user.tipo == 'funcionario' or request.user.tipo == 'profissional' or request.user.is_staff:
        # Busca todos os agendamentos do dia atual (independente da hora)
        agendamentos_hoje = Agendamento.objects.filter(
            data_horario__date=hoje
        ).exclude(status='CA')

        # Se for um funcionário comum, filtra apenas os agendamentos vinculados ao perfil dele
        if not request.user.is_staff:
            try:
                perfil = Funcionario.objects.get(user=request.user)
                agendamentos_hoje = agendamentos_hoje.filter(funcionario=perfil)
            except Funcionario.DoesNotExist:
                # Se o usuário não tiver um perfil de funcionário criado no Admin
                agendamentos_hoje = Agendamento.objects.none()

        # Variáveis que o seu HTML utiliza para o painel azul e a tabela
        context['agendamentos_hoje_count'] = agendamentos_hoje.count()
        context['agendamentos_hoje_list'] = agendamentos_hoje.order_by('data_horario')

    # Renderiza o template enviando todos os dados organizados no 'context'
    return render(request, 'painel/dashboard.html', context)