from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = [
            'id',
            'categoria',
            'produtor',
            'nome',
            'descricao',
            'quantidade_total',
            'quantidade_reservada',
            'preco',
            'ativo'
        ]
        read_only_fields = ['id', 'produtor']

    def validate_quantidade_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantidade total deve ser maior que zero")
        return value

    def validate_quantidade_reservada(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantidade reservada não pode ser negativa")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        if not hasattr(user, 'produtor'):
            raise serializers.ValidationError("Usuário não é produtor")

        validated_data.pop('id_produtor', None)

        return Produto.objects.create(
            id_produtor=user.produtor,
            **validated_data
        )