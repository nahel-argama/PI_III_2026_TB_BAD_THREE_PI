from rest_framework import serializers
from .models import Avaliacao

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id_avaliacao', 'id_pedido', 'id_produto', 'id_produtor', 'id_varejista', 'nota', 'comentario', 'criado_em']
        read_only_fields = ['id_avaliacao', 'criado_em']

    def validate_nota(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("A nota deve ser entre 0 e 5.")
        return value