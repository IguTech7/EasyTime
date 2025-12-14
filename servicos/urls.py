from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.listar_servicos, name='listar'),
    path('novo/', views.criar_servico, name='criar'),
    path('editar/<int:pk>/', views.editar_servico, name='editar'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir'),
]