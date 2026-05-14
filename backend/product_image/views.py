from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from image.models import Image
from product.models import Product
from product_image.models import ProductImage
from product_image.serializers import (
    ProductImageSerializer,
    ProductImageUploadSerializer,
)
from users.permissions import IsProducer


class ProductImageListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsProducer()]
        return [IsAuthenticated()]

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        images = ProductImage.objects.filter(product=product).order_by("id")
        serializer = ProductImageSerializer(
            images, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        producer = request.user.producer

        product = Product.objects.filter(id=product_id, producer=producer).first()

        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload = serializer.validated_data["image"]

        with transaction.atomic():
            image = Image.objects.create(
                blob=upload.read(),
                mime_type=upload.content_type or "application/octet-stream",
            )

            product_image = ProductImage.objects.create(product=product, image=image)

        response_serializer = ProductImageSerializer(
            product_image, context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
