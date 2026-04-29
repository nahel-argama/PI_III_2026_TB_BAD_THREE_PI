from .models import ItemPedido
from rest_framework import serializers

class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'quantidade', 'preco_unitario']
        read_only_fields = ['id']

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate_pedido(self, value):
        user = self.context['request'].user

        if user.type == 'VAREJISTA' and value.varejista != user.varejista:
            raise serializers.ValidationError("Pedido não pertence ao usuário.")

        return value