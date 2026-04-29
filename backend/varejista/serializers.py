from rest_framework import serializers
from .models import Varejista


class VarejistaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Varejista
        fields = [
            'user',
            'tipo_documento',
            'documento'
        ]
        read_only_fields = ['user']

    def validate_tipo_documento(self, value):
        if value not in ['CPF', 'CNPJ']:
            raise serializers.ValidationError("Tipo de documento inválido.")
        return value

    def validate_documento(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Documento deve conter apenas números.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        tipo_documento = data.get('tipo_documento')
        documento = data.get('documento')

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        if user.type != 'VAREJISTA':
            raise serializers.ValidationError("Usuário deve ser do tipo VAREJISTA")

        if self.instance is None and hasattr(user, 'varejista'):
            raise serializers.ValidationError("Usuário já possui cadastro de Varejista")

        if tipo_documento == 'CPF' and len(documento) != 11:
            raise serializers.ValidationError({"documento": "CPF deve ter 11 dígitos."})

        if tipo_documento == 'CNPJ' and len(documento) != 14:
            raise serializers.ValidationError({"documento": "CNPJ deve ter 14 dígitos."})

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Varejista.objects.create(user=user, **validated_data)