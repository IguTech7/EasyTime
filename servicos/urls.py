from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.listar_servicos, name='listar'),
    path('novo/', views.criar_servico, name='criar'),
]
