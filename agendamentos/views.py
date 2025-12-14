from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from agendamentos.forms import AgendamentoForm
from agendamentos.models import Agendamento, Funcionario, Servico
from datetime import date, datetime, time, timedelta

STATUS_CANCELADO = 'CA'

def is_funcionario_or_staff(user):
    return user.is_staff or user.tipo == 'funcionario'

def can_view_agendamento(user, agendamento):
    if user.is_staff:
        return True
    if user == agendamento.usuario:
        return True
    
    try:
        funcionario_perfil = Funcionario.objects.get(user=user)
        return funcionario_perfil == agendamento.funcionario
    except Funcionario.DoesNotExist:
        return False

@login_required
def detalhar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    if not can_view_agendamento(request.user, agendamento):
        messages.error(request, "Você não tem permissão para visualizar este agendamento.")
        return redirect('painel:dashboard')
        
    context = {
        'agendamento': agendamento
    }
    return render(request, 'agendamentos/detalhar_agendamento.html', context)

def checar_disponibilidade(request):
    funcionario_id = request.GET.get('funcionario')
    data_str = request.GET.get('data')
    servico_id = request.GET.get('servico')

    if not all([funcionario_id, data_str, servico_id]):
        return JsonResponse({'disponivel': False, 'erro': 'Dados insuficientes.'}, status=400)

    try:
        funcionario = Funcionario.objects.get(pk=funcionario_id)
        servico = Servico.objects.get(pk=servico_id)
        data_escolhida = datetime.strptime(data_str, '%Y-%m-%d').date()
    except (Funcionario.DoesNotExist, Servico.DoesNotExist):
        return JsonResponse({'disponivel': False, 'erro': 'Funcionário ou Serviço inválido.'}, status=404)
        
    HORA_INICIO_TRABALHO = 9
    HORA_FIM_TRABALHO = 18
    INTERVALO_MINUTOS = 30

    horarios_disponiveis = []
    
    start_time = datetime.combine(data_escolhida, datetime.min.time()) + timedelta(hours=HORA_INICIO_TRABALHO)
    end_time = datetime.combine(data_escolhida, datetime.min.time()) + timedelta(hours=HORA_FIM_TRABALHO)
    
    current_time = start_time
    
    agendamentos_ocupados = Agendamento.objects.filter(
        funcionario=funcionario,
        data_horario__date=data_escolhida,
    ).exclude(status=STATUS_CANCELADO)

    while current_time < end_time:
        horario = current_time.time().strftime('%H:%M')
        
        duracao_servico = timedelta(minutes=servico.duracao)
        fim_servico = current_time + duracao_servico

        esta_disponivel = True
        
        for agendamento in agendamentos_ocupados:
            inicio_existente = agendamento.data_horario
            duracao_existente = timedelta(minutes=agendamento.servico.duracao)
            fim_existente = inicio_existente + duracao_existente

            if current_time < fim_existente and fim_servico > inicio_existente:
                esta_disponivel = False
                break
        
        if esta_disponivel:
            horarios_disponiveis.append(horario)
            
        current_time += timedelta(minutes=INTERVALO_MINUTOS)

    return JsonResponse({'horarios': horarios_disponiveis})

@login_required(login_url='usuarios:login')
def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            
            data_str = form.cleaned_data['data_agendamento']
            hora_str = form.cleaned_data['hora_agendamento']
            
            try:
                data_hora_completa_str = f"{data_str} {hora_str}"
                data_hora_agendamento = datetime.strptime(data_hora_completa_str, '%Y-%m-%d %H:%M')
            except ValueError:
                messages.error(request, "Formato de data ou hora inválido.")
                return render(request, 'agendamentos/criar_agendamento.html', {'form': form, 'titulo': 'Agendar Serviço', 'botao_submit': 'Solicitar Agendamento'})

            agendamento.usuario = request.user
            agendamento.data_horario = data_hora_agendamento
            
            agendamento.save()
            messages.success(request, 'Seu agendamento foi solicitado com sucesso! Aguardando confirmação.')
            return redirect('painel:dashboard')
        else:
            messages.error(request, 'Ocorreu um erro na submissão do formulário. Por favor, verifique os campos.')
    else:
        initial_data = {}
        servico_pk = request.GET.get('servico')
        if servico_pk:
            initial_data['servico'] = servico_pk
        
        form = AgendamentoForm(initial=initial_data)
        
    context = {
        'form': form,
        'titulo': 'Agendar Serviço',
        'botao_submit': 'Solicitar Agendamento'
    }
    return render(request, 'agendamentos/criar_agendamento.html', context)

@login_required(login_url='usuarios:login')
def listar_agendamentos_cliente(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('data_horario')
    
    context = {
        'agendamentos': agendamentos,
        'titulo': 'Meus Agendamentos'
    }
    return render(request, 'agendamentos/listar_agendamentos_cliente.html', context)

@never_cache
@login_required(login_url='usuarios:login')
@user_passes_test(is_funcionario_or_staff, login_url='/painel/')
def agenda_do_dia(request):
    data_selecionada = date.today()
    data_param = request.GET.get('data')
    
    if data_param:
        try:
            data_selecionada = datetime.strptime(data_param, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido. Exibindo agenda de hoje.")

    inicio_do_dia = datetime.combine(data_selecionada, time.min)
    fim_do_dia = datetime.combine(data_selecionada, time.max)

    agendamentos = Agendamento.objects.filter(
        data_horario__range=(inicio_do_dia, fim_do_dia)
    ).exclude(status='CA').order_by('data_horario')

    if request.user.tipo == 'funcionario' and not request.user.is_staff:
        try:
            perfil_funcionario = Funcionario.objects.get(user=request.user)
            agendamentos = agendamentos.filter(funcionario=perfil_funcionario)
        except Funcionario.DoesNotExist:
            agendamentos = Agendamento.objects.none()

    context = {
        'agendamentos': agendamentos,
        'data_selecionada': data_selecionada,
    }
    return render(request, 'agendamentos/agenda.html', context)

@login_required(login_url='usuarios:login')
def cancelar_agendamento(request, pk):
    
    if request.user.is_staff or request.user.tipo == 'funcionario':
        agendamento = get_object_or_404(Agendamento, pk=pk)
        redirect_url = 'agendamentos:agenda'
    else:
        agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
        redirect_url = 'agendamentos:listar'
    
    if agendamento.status != STATUS_CANCELADO:
        agendamento.status = STATUS_CANCELADO
        agendamento.save()
        
        if request.user.is_staff or request.user.tipo == 'funcionario':
            messages.success(request, f'Agendamento do cliente {agendamento.usuario.username} cancelado com sucesso.')
        else:
            messages.success(request, f'Seu agendamento do serviço "{agendamento.servico.nome}" foi cancelado com sucesso.')
    else:
        messages.warning(request, 'Este agendamento já estava cancelado.')
        
    return redirect(redirect_url)

@login_required(login_url='usuarios:login')
@user_passes_test(lambda u: u.is_staff or u.tipo == 'funcionario', login_url='/painel/')
def marcar_como_realizado(request, pk):
    if request.method == 'POST':
        agendamento = get_object_or_404(Agendamento, pk=pk)
        
        agendamento.status = 'RE'
        agendamento.save()
        
        messages.success(request, f"Agendamento de {agendamento.usuario.get_full_name()} marcado como REALIZADO.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('painel:dashboard')))

@login_required(login_url='usuarios:login')
@user_passes_test(lambda u: u.is_staff or u.tipo == 'funcionario', login_url='/painel/')
def confirmar_agendamento(request, pk):
    if request.method == 'POST':
        agendamento = get_object_or_404(Agendamento, pk=pk)
        
        if agendamento.status == 'PE':
            agendamento.status = 'AG'
            agendamento.save()
            messages.success(request, f"Agendamento de {agendamento.usuario.get_full_name()} CONFIRMADO com sucesso.")
        else:
            messages.error(request, "Este agendamento já está confirmado ou não está Pendente.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('painel:dashboard')))