from rest_framework import viewsets, mixins
from .serializers import OrderItemSerializer
from users.permissions import IsRetailer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderItemFilter
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem

class OrderItemViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter

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