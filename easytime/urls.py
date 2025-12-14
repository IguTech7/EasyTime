from django.contrib import admin
from django.urls import path, include
from painel.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('servicos/', include('servicos.urls', namespace='servicos')),
    path('agendamentos/', include('agendamentos.urls', namespace='agendamentos')),
    path('funcionarios/', include('funcionarios.urls', namespace='funcionarios')),
    path('painel/', include('painel.urls', namespace='painel')),
]