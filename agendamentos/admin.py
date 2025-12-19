from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servico', 'funcionario', 'data_horario', 'status')
    list_filter = ('status', 'data_horario', 'funcionario', 'servico')
    search_fields = ('usuario__username', 'funcionario__nome', 'servico__nome')
    date_hierarchy = 'data_horario'