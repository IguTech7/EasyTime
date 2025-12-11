from django.urls import path
from . import views

app_name = "painel"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-funcionario/', views.dashboard_funcionario, name='dashboard_funcionario'),
]
