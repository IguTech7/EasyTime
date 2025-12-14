from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('', views.listar_funcionarios, name='listar'),
    path('criar/', views.criar_funcionario, name='criar'),
    path('editar/<int:pk>/', views.editar_funcionario, name='editar'),
    path('excluir/<int:pk>/', views.excluir_funcionario, name='excluir'),
]