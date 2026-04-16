from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.Serializer):

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'id_varejista', 'status', 'valor_total', 'criado_em']
        read_only_fields = ['id_pedido', 'id_varejista', 'criado_em']

    def validate_valor_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor total deve ser maior que zero.")
        return value