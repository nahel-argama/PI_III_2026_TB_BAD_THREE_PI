from django.db import models
from pedido.models import Pedido

class ItemPedido(models.Model):
    id_item = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(to=Pedido, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id_item} - Pedido: {self.id_pedido.id_pedido} - Quantidade: {self.quantidade} - Preço Unitário: {self.preco_unitario}"