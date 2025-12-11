from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.listar_agendamentos, name='listar'),
    path('novo/', views.criar_agendamento, name='criar'),
]
