from rest_framework import serializers
from .models import Endereco

class EnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = [
            'id_endereco',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'cep'
        ]

    def validate_cep(self, value):
        value = value.replace('-', '')

        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("CEP deve ter 8 dígitos")

        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        return Endereco.objects.create(user=user, **validated_data)