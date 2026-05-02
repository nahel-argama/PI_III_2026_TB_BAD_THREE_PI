from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'producer',
            'name',
            'description',
            'total_quantity',
            'reserved_quantity',
            'price',
            'is_active'
        ]
        read_only_fields = ['id', 'producer']

    def validate_total_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total quantity must be greater than zero")
        return value

    def validate_reserved_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Reserved quantity cannot be negative")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")

        if not hasattr(user, 'producer'):
            raise serializers.ValidationError("User is not a producer")

        validated_data.pop('producer', None)

        return Product.objects.create(
            producer=user.producer,
            **validated_data
        )