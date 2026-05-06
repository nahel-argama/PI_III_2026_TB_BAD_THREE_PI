from .models import OrderItem
from rest_framework import serializers
from order.services import validate_item_stock

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ['id', 'order', 'unit_price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_order(self, value):
        user = self.context['request'].user

        if user.user_type == 'RETAILER' and value.retailer != user.retailer:
            raise serializers.ValidationError("Order does not belong to the user.")

        if value.status != 'PENDING':
            raise serializers.ValidationError("Only pending orders can be modified.")

        return value

    def validate(self, data):
        product = data.get('product') or getattr(self.instance, 'product', None)
        order = data.get('order') or getattr(self.instance, 'order', None)
        quantity = data.get('quantity') or getattr(self.instance, 'quantity', None)

        if product and order and product.producer != order.producer:
            raise serializers.ValidationError("Product producer must match order producer.")

        if product and quantity:
            stock_error = validate_item_stock(product, quantity)
            if stock_error:
                raise serializers.ValidationError({"quantity": stock_error})

        return data

    def create(self, validated_data):
        validated_data['unit_price'] = validated_data['product'].price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('unit_price', None)
        if 'product' in validated_data:
            validated_data['unit_price'] = validated_data['product'].price
        return super().update(instance, validated_data)
