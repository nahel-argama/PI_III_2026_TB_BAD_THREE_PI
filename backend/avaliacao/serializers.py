from rest_framework import serializers
from .models import Avaliacao

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'pedido', 'produto', 'produtor', 'varejista', 'nota', 'comentario', 'criado_em']
        read_only_fields = ['id', 'criado_em']

    def validate_nota(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("A nota deve ser entre 0 e 5.")
        return value