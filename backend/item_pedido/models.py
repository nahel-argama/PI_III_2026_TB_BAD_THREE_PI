from django.db import models
from django.db.models import Sum, F
from pedido.models import Pedido

def atualizar_total(pedido):
    total = pedido.itens.aggregate(
        total=Sum(F('quantidade') * F('preco_unitario'))
    )['total'] or 0

    pedido.valor_total = total
    pedido.save()

class ItemPedido(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_item")
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        atualizar_total(self.pedido)

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        atualizar_total(pedido)