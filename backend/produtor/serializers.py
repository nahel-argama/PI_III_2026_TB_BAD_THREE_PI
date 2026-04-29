from rest_framework import serializers
from .models import Produtor


class ProdutorSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Produtor
        fields = [
            'user_id',
            'tipo_documento',
            'documento',
            'nome_fantasia'
        ]

    def validate(self, data):
        user = self.context['request'].user
        tipo_documento = data.get('tipo_documento')
        documento = data.get('documento')

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado")

        if user.type != 'PRODUTOR':
            raise serializers.ValidationError("Usuário deve ser do tipo PRODUTOR")

        if hasattr(user, 'produtor'):
            raise serializers.ValidationError("Usuário já possui cadastro de Produtor")

        if tipo_documento == 'CPF' and len(documento) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")
        if tipo_documento == 'CNPJ' and len(documento) != 14:
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")

        return data

    def create(self, validated_data):
        return Produtor.objects.create(**validated_data)