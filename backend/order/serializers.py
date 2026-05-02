from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'retailer', 'status', 'total_value', 'created_at']
        read_only_fields = ['id', 'retailer', 'total_value', 'created_at']

    def validate(self, data):
        if self.instance and self.instance.status in ['CANCELED', 'DELIVERED']:
            raise serializers.ValidationError("Cannot modify this order.")
        return data