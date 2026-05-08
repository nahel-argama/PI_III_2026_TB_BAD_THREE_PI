from rest_framework import serializers
from .models import Producer


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ["document_type", "document_number", "trade_name"]

    def validate(self, data):
        document_type = data.get("document_type")
        document_number = data.get("document_number")

        if document_type == "CPF" and len(document_number) != 11:
            raise serializers.ValidationError(
                {"document_number": "CPF must have 11 digits."}
            )

        if document_type == "CNPJ" and len(document_number) != 14:
            raise serializers.ValidationError(
                {"document_number": "CNPJ must have 14 digits."}
            )

        return data

    def create(self, validated_data):
        return Producer.objects.create(**validated_data)
