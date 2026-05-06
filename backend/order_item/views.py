from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .serializers import OrderItemSerializer
from .filters import OrderItemFilter
from .models import OrderItem

from users.permissions import IsRetailer
from order.models import Order
from order.services import validate_item_stock


class OrderItemViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsRetailer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = OrderItem.objects.all()

        order_id = self.kwargs.get('order_pk')
        if order_id:
            queryset = queryset.filter(order_id=order_id)

        if user.user_type == 'RETAILER':
            return queryset.filter(order__retailer=user.retailer)

        if user.user_type == 'PRODUCER':
            return queryset.filter(product__producer=user.producer)

        return OrderItem.objects.none()

    def get_order(self):
        order_id = self.kwargs.get('order_pk')
        user = self.request.user
        try:
            return Order.objects.get(pk=order_id, retailer=user.retailer)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = self.get_order()

        if order.status != 'PENDING':
            raise ValidationError("Cannot add items to non-pending order")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if product.producer != order.producer:
            raise ValidationError({
                'non_field_errors': ["Product producer must match order producer."]
            })

        existing_item = OrderItem.objects.filter(
            order=order,
            product=product
        ).first()

        if existing_item:
            total_quantity = existing_item.quantity + quantity
            error = validate_item_stock(product, total_quantity)
            if error:
                raise ValidationError(error)

            existing_item.quantity = total_quantity
            existing_item.save()
            out = self.get_serializer(existing_item)
            return Response(out.data, status=status.HTTP_201_CREATED)

        error = validate_item_stock(product, quantity)
        if error:
            raise ValidationError(error)

        item = serializer.save(order=order, unit_price=product.price)
        return Response(self.get_serializer(item).data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        order = serializer.instance.order

        if order.status != 'PENDING':
            raise ValidationError("Cannot modify non-pending order")

        product = serializer.instance.product
        quantity = serializer.validated_data.get('quantity', serializer.instance.quantity)

        error = validate_item_stock(product, quantity)
        if error:
            raise ValidationError(error)

        serializer.save()

    def perform_destroy(self, instance):
        if instance.order.status != 'PENDING':
            raise ValidationError("Cannot delete item from non-pending order")
        instance.delete()
