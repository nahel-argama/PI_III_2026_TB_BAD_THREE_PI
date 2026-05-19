from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from image.models import Image
from product.models import Product
from product_image.models import ProductImage
from product_image.serializers import (
    ProductImageSerializer,
    ProductImageUploadSerializer,
)
from users.permissions import IsProducer


class ProductImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsProducer()]
        return [IsAuthenticated()]

    def list(self, request, product_pk=None):
        product = Product.objects.filter(id=product_pk).first()
        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        images = ProductImage.objects.filter(product=product).order_by("id")
        serializer = ProductImageSerializer(
            images, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, product_pk=None):
        producer = request.user.producer

        product = Product.objects.filter(id=product_pk, producer=producer).first()

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


class ProductImageDeleteView(APIView):
    def get_permissions(self):
        return [IsProducer()]

    def delete(self, request, product_id, image_id):
        producer = request.user.producer

        product = Product.objects.filter(id=product_id, producer=producer).first()
        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

        product_image = ProductImage.objects.filter(
            product=product, id=image_id
        ).first()
        if not product_image:
            return Response(
                {"detail": "Product image not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        image = product_image.image

        with transaction.atomic():
            product_image.delete()
            image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
