from rest_framework import viewsets, mixins
from .serializers import OrderItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderItemFilter
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem
from users.permissions import IsRetailer

class OrderItemViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsRetailer()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'RETAILER':
            return OrderItem.objects.filter(
                order__retailer=user.retailer
            )

        if user.user_type == 'PRODUCER':
            return OrderItem.objects.filter(
                product__producer=user.producer
            )

        return OrderItem.objects.none()
