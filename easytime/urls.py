from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
   path('', lambda request: redirect('painel:dashboard')),

    path('admin/', admin.site.urls),

    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('painel/', include('painel.urls', namespace='painel')),
    path('servicos/', include('servicos.urls', namespace='servicos')),
    path('agendamentos/', include('agendamentos.urls', namespace='agendamentos')),
]
