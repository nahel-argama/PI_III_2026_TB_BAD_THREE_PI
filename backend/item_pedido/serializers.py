from .models import ItemPedido
from rest_framework import serializers

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id_item', 'id_pedido', 'quantidade', 'preco_unitario']
        read_only_fields = ['id_item']

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value