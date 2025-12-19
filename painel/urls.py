from django.urls import path
from . import views

app_name = 'painel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),
    path('perfil/atualizar/', views.atualizar_perfil_profissional, name='atualizar_perfil'),
    path('atualizar-especialidades/', views.atualizar_especialidades, name='atualizar_especialidades'),
]