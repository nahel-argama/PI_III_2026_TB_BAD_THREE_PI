from rest_framework import viewsets, mixins
from .serializers import OrderSerializer
from users.permissions import IsRetailer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from order_item.serializers import OrderItemSerializer
from .models import Order

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
        if self.action in ['create']:
            return [IsAuthenticated(), IsRetailer()]

        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        user = request.user

        if user.user_type == 'RETAILER':
            items = order.items.all()

        elif user.user_type == 'PRODUCER':
            items = order.items.filter(
                product__producer=user.producer
            )

        else:
            items = []

        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'RETAILER':
            return Order.objects.filter(retailer=user.retailer)

        if user.user_type == 'PRODUCER':
            return Order.objects.filter(
                items__product__producer=user.producer
            ).distinct()

        return Order.objects.none()