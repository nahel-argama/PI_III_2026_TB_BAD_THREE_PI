from rest_framework import serializers
from .models import Order
from order_item.serializers import OrderItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'retailer', 'producer', 'status', 'total_value', 'items', 'created_at']
        read_only_fields = ['id', 'retailer', 'total_value', 'created_at', 'items']

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
