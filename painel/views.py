from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
from django.utils import timezone
from django.shortcuts import redirect


@login_required
def dashboard_cliente(request):
    agendamentos = Agendamento.objects.filter(cliente=request.user)

    total = agendamentos.count()
    futuros = agendamentos.filter(data__gte=timezone.now().date()).count()
    ultimo = agendamentos.order_by('-data').first()

    return render(request, 'painel/dashboard_cliente.html', {
        'total': total,
        'futuros': futuros,
        'ultimo': ultimo,
        'agendamentos': agendamentos.order_by('data')[:5],
    })
@login_required
def dashboard_funcionario(request):
    # Aqui você vai colocar os dados reais depois
    context = {
        'total_agendamentos': 0,
        'proximos_agendamentos': [],
        'meus_servicos': [],
    }
    return render(request, 'painel/dashboard_funcionario.html', context)

@login_required
def escolher_dashboard(request):
    if request.user.tipo == 'cliente':
        return redirect('painel:dashboard_cliente')
    elif request.user.tipo == 'funcionario':
        return redirect('painel:dashboard_funcionario')
