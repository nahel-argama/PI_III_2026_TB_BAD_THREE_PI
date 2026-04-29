from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ['id', 'varejista', 'status', 'valor_total', 'criado_em']
        read_only_fields = ['id', 'varejista', 'valor_total', 'criado_em']

    def validate(self, data):
        if self.instance and self.instance.status in ['CANCELADO', 'ENTREGUE']:
            raise serializers.ValidationError("Não é possível alterar este pedido.")
        return data