from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import OrderSerializer
from users.permissions import IsRetailer
from .filters import OrderFilter
from .models import Order
from .services import confirm_order_with_stock


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'confirm', 'cancel']:
            return [IsAuthenticated(), IsRetailer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'RETAILER':
            return Order.objects.filter(
                retailer=user.retailer
            ).prefetch_related('items')

        if user.user_type == 'PRODUCER':
            return Order.objects.filter(
                producer=user.producer
            ).prefetch_related('items').distinct()

        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(retailer=self.request.user.retailer)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()

        if order.status != 'PENDING':
            return Response(
                {"error": f"Order status is {order.status}, not PENDING"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not order.items.exists():
            return Response(
                {"error": "Cannot confirm order with no items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order, error = confirm_order_with_stock(order)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status in ['CANCELED', 'DELIVERED']:
            return Response(
                {"error": f"Cannot cancel order with status {order.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELED'
        order.save()

        return Response(OrderSerializer(order).data)