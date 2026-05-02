from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'number',
            'complement',
            'neighborhood',
            'city',
            'state',
            'postal_code'
        ]

    def validate_postal_code(self, value):
        value = value.replace('-', '')

        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("Postal code must have 8 digits")

        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")

        return Address.objects.create(user=user, **validated_data)