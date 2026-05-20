from rest_framework import serializers

from product import price_scrapper_client
from product.price_scrapper_client import ExternalServiceError
from product_image.serializers import ProductImageSerializer
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    distance_km = serializers.SerializerMethodField()
    external_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'producer',
            'external_id',
            'name',
            'description',
            'total_quantity',
            'reserved_quantity',
            'price',
            'is_active',
            'images',
            'distance_km',
        ]
        read_only_fields = ['id', 'producer', 'name', 'distance_km']

    def get_distance_km(self, obj):
        distance = getattr(obj, 'distance_km', None)
        if distance is None:
            return None
        return round(float(distance), 2)

    def validate_total_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total quantity must be greater than zero")
        return value

    def validate_reserved_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Reserved quantity cannot be negative")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value

    def validate_external_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("External ID cannot be blank")
        return value

    def validate(self, data):
        if 'name' in self.initial_data:
            raise serializers.ValidationError(
                {'name': 'Send external_id instead of name.'}
            )

        total_quantity = data.get(
            'total_quantity',
            self.instance.total_quantity if self.instance else None
        )
        reserved_quantity = data.get(
            'reserved_quantity',
            self.instance.reserved_quantity if self.instance else 0
        )

        if (
            total_quantity is not None and
            reserved_quantity is not None and
            reserved_quantity > total_quantity
        ):
            raise serializers.ValidationError(
                "Reserved quantity cannot be greater than total quantity"
            )

        external_id = data.get('external_id')
        if external_id:
            data['name'] = self.get_external_product_name(external_id)
        elif self.instance is None:
            raise serializers.ValidationError(
                {'external_id': 'This field is required.'}
            )

        return data

    def get_external_product_name(self, external_id):
        response = price_scrapper_client.get_product_by_id(external_id)

        if isinstance(response, ExternalServiceError):
            raise serializers.ValidationError({"external_id": response.message})

        if response.status != 200:
            raise serializers.ValidationError(
                {
                    "external_id": (
                        "Failed to retrieve product information from external service."
                    )
                }
            )

        return response.data["name"]

    def create(self, validated_data):
        user = self.context['request'].user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")

        if not hasattr(user, 'producer'):
            raise serializers.ValidationError("User is not a producer")

        validated_data.pop('producer', None)
        validated_data.pop('external_id', None)

        return Product.objects.create(
            producer=user.producer,
            **validated_data
        )

    def update(self, instance, validated_data):
        validated_data.pop('producer', None)
        validated_data.pop('external_id', None)

        return super().update(instance, validated_data)
