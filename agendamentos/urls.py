from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('agendar/', views.criar_agendamento, name='criar'),
    path('meus/', views.listar_agendamentos_cliente, name='listar'), 
    path('disponibilidade/', views.checar_disponibilidade, name='disponibilidade'),
    path('agenda/', views.agenda_do_dia, name='agenda'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar'),
    path('detalhes/<int:pk>/', views.detalhar_agendamento, name='detalhes'),
    path('marcar_realizado/<int:pk>/', views.marcar_como_realizado, name='marcar_realizado'),
    path('confirmar/<int:pk>/', views.confirmar_agendamento, name='confirmar_agendamento'),
]