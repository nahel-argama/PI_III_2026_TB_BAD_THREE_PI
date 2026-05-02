from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsProducer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ProductFilter


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("producer", "category")
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["price", "name"]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsProducer]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, "producer"):
            return Product.objects.filter(producer=user.producer)

        if hasattr(user, "retailer"):
            return Product.objects.filter(is_active=True)

        return Product.objects.none()
