from rest_framework import serializers
from .models import Order
from order_item.serializers import OrderItemSerializer
from producer.models import Producer
from retailer.models import Retailer


class ProducerSummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = Producer
        fields = [
            'id',
            'name',
            'trade_name',
            'email',
            'document_type',
            'document_number',
            'address',
        ]

    def get_address(self, obj):
        address = getattr(obj.user, 'address', None)
        if not address:
            return None

        return {
            'street': address.street,
            'number': address.number,
            'complement': address.complement,
            'neighborhood': address.neighborhood,
            'city': address.city,
            'state': address.state,
            'postal_code': address.postal_code,
        }


class RetailerSummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = Retailer
        fields = [
            'id',
            'name',
            'trade_name',
            'email',
            'document_type',
            'document_number',
            'address',
        ]

    def get_address(self, obj):
        address = getattr(obj.user, 'address', None)
        if not address:
            return None

        return {
            'street': address.street,
            'number': address.number,
            'complement': address.complement,
            'neighborhood': address.neighborhood,
            'city': address.city,
            'state': address.state,
            'postal_code': address.postal_code,
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    producer_data = ProducerSummarySerializer(source='producer', read_only=True)
    retailer_data = RetailerSummarySerializer(source='retailer', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'retailer',
            'retailer_data',
            'producer',
            'producer_data',
            'status',
            'subtotal_value',
            'fee_value',
            'total_value',
            'items',
            'created_at',
        ]
        read_only_fields = ['id', 'retailer', 'subtotal_value', 'fee_value', 'total_value', 'created_at', 'items']

    def validate(self, data):
        if not self.instance:
            user = self.context['request'].user
            producer = data.get('producer')

            if producer and Order.objects.filter(
                retailer=user.retailer,
                producer=producer,
                status='PENDING'
            ).exists():
                raise serializers.ValidationError(
                    "There is already a pending order for this producer."
                )

        if self.instance and self.instance.status in ['CANCELED', 'DELIVERED']:
            raise serializers.ValidationError("Cannot modify this order.")
        return data
