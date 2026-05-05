from rest_framework import serializers
from .models import Order
from order_item.serializers import OrderItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'retailer', 'producer', 'status', 'total_value', 'items', 'created_at']
        read_only_fields = ['id', 'retailer', 'producer', 'total_value', 'created_at', 'items']

    def validate(self, data):
        if self.instance and self.instance.status in ['CANCELED', 'DELIVERED']:
            raise serializers.ValidationError("Cannot modify this order.")
        return data