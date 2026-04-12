from rest_framework import serializers
from .models import Endereco
from estado.models import Estado

class EnderecoSerializer(serializers.ModelSerializer):
    estado_id = serializers.PrimaryKeyRelatedField(
        source='estado',
        queryset=Estado.objects.all()
    )

    class Meta:
        model = Endereco
        fields = [
            'id_endereco',
            'estado_id',
            'rua',
            'numero',
            'bairro',
            'cidade',
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