# funcionarios/admin.py (CORRIGIDO)
from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone') # Exemplo com telefone, ajuste conforme seu modelo
    search_fields = ('nome',)