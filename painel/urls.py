from django.urls import path
from . import views

app_name = 'painel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),
]