from rest_framework import serializers
from .models import Producer


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = [
            'user',
            'document_type',
            'document_number',
            'trade_name'
        ]
        read_only_fields = ['user']

    def validate_document_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Document must contain only numbers.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        document_type = data.get('document_type')
        document_number = data.get('document_number')

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")

        if user.user_type != 'PRODUCER':
            raise serializers.ValidationError("User must be a PRODUCER")

        if self.instance is None and hasattr(user, 'producer'):
            raise serializers.ValidationError("User already has a producer profile")

        if document_type == 'CPF' and len(document_number) != 11:
            raise serializers.ValidationError({"document_number": "CPF must have 11 digits."})

        if document_type == 'CNPJ' and len(document_number) != 14:
            raise serializers.ValidationError({"document_number": "CNPJ must have 14 digits."})

        return data

    def create(self, validated_data):
        return Producer.objects.create(**validated_data)