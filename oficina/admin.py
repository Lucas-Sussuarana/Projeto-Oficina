from django.contrib import admin
from .models import (
    Cliente,
    Veiculo,
    Peca,
    Servico,
    OrdemServico,
    ItemServico,
    ItemPeca,
    ParticipacaoMecanico,
    Observacao,
    MovimentacaoEstoque,
)

class ItemPecaAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user

        super().save_model(request, obj, form, change)

admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Peca)
admin.site.register(Servico)
admin.site.register(OrdemServico)
admin.site.register(ItemServico)
admin.site.register(ItemPeca, ItemPecaAdmin)
admin.site.register(ParticipacaoMecanico)
admin.site.register(Observacao)
admin.site.register(MovimentacaoEstoque)