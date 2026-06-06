from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request
import rest_framework.status as status
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductDescriptionGenerateSerializer
from . import gemini_client
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
    queryset = Product.objects.select_related(
        "producer",
        "producer__user",
        "producer__user__address",
        "category",
    )
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["price", "name", "created_at", "distance_km"]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsProducer]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == "PRODUCER":
            return self.queryset.filter(
                producer=user.producer, is_active=True
            ).order_by("id")

        if user.user_type == "RETAILER":
            from django.db.models import F

            return self.queryset.filter(
                is_active=True, total_quantity__gt=F("reserved_quantity")
            ).order_by("id")

        return Product.objects.none()


class ProductDescriptionGenerateView(APIView):
    serializer_class = ProductDescriptionGenerateSerializer
    permission_classes = [IsProducer]

    def post(self, request, *args, **kwargs):
        product_name = request.data.get("product_name")

        description = gemini_client.generate_product_description(
            product_name=product_name
        )

        return Response(data={"description": description}, status=status.HTTP_200_OK)
