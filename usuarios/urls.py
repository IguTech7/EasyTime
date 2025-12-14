from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', LogoutView.as_view(), name='logout'),
]