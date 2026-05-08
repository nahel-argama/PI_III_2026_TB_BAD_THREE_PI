from rest_framework import serializers
from wishlist.models import Wishlist
from .models import Retailer


class RetailerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Retailer
        fields = ["document_type", "document_number", "trade_name"]

    def validate_document_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Document must contain only numbers.")
        return value

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
        retailer = Retailer.objects.create(**validated_data)
        Wishlist.objects.get_or_create(retailer=retailer)
        return retailer
