from .models import OrderItem
from rest_framework import serializers
from product.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_order(self, value):
        user = self.context['request'].user

        if user.user_type == 'RETAILER' and value.retailer != user.retailer:
            raise serializers.ValidationError("Order does not belong to the user.")

        return value

    def validate(self, data):
        product = data.get('product')
        order = data.get('order') or self.instance.order

        if product and product.producer != order.producer:
            raise serializers.ValidationError("Product producer must match order producer.")

        return data