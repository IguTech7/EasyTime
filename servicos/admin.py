from django.contrib import admin
from .models import Servico

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao') 
    list_filter = ('duracao',)
    search_fields = ('nome', 'descricao')
    

    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao')
        }),
        ('Detalhes do Serviço', {
            'fields': ('preco', 'duracao')
        }),
    )

admin.site.register(Servico, ServicoAdmin)