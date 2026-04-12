from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = [
            'id_produto',
            'nome',
            'descricao',
            'preco',
            'estoque',
            'ativo'
        ]

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError("Preço deve ser maior que zero")
        return value

    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError("Estoque não pode ser negativo")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        if not hasattr(user, 'produtor'):
            raise serializers.ValidationError("Usuário não é produtor")

        return Produto.objects.create(
            produtor=user.produtor,
            **validated_data
        )