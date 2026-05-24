from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from django.db import transaction

from product import price_scrapper_client as product_client
from default_product_image.models import DefaultProductImage
from default_product_image.serializers import (
    DefaultProductImageSerializer,
    DefaultProductImageUploadSerializer,
)
from image.models import Image
from default_product_image.filters import DefaultProductImageFilter
from default_product_image import image_generation
import config.settings as settings
from default_product_image.throttles import DefaultProductImageGenerationThrottle


class DefaultProductImageListView(APIView):
    permission_classes = [IsAdminUser]
    filterset_class = DefaultProductImageFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return DefaultProductImage.objects.select_related("image").order_by("id")

    def get(self, request):
        queryset = self.get_queryset()

        filterset = self.filterset_class(
            data=request.query_params, queryset=queryset, request=request
        )

        queryset = filterset.qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = DefaultProductImageSerializer(
            page, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)


class DefaultProductImageUploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, product_external_key):
        serializer = DefaultProductImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload = serializer.validated_data["image"]
        external_response = product_client.get_product_by_id_validated(
            product_external_key
        )
        product_name = external_response.data["name"]

        default_image = self.store_new_image(product_name, product_external_key, upload)

        response_serializer = DefaultProductImageSerializer(
            default_image, context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def store_new_image(self, product_name, product_external_key, upload):
        with transaction.atomic():
            default_image, was_created = DefaultProductImage.objects.get_or_create(
                product_external_key=product_external_key,
                defaults={"product_name": product_name},
            )

            image = Image.objects.create(
                blob=upload.read(),
                mime_type=upload.content_type or "application/octet-stream",
            )

            old_image = default_image.image
            default_image.image = image
            default_image.save(update_fields=["image", "product_name"])

            if not old_image:
                return default_image

            if old_image.product_images.exists():
                return default_image

            old_image.delete()

        return default_image


class DefaultProductImageGenerateView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [DefaultProductImageGenerationThrottle]

    def get(self, request, product_external_key):
        if not settings.ENABLE_DEFAULT_IMAGE_GENERATION:
            return Response(
                {"detail": "External product image generation is disabled."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        product = product_client.get_product_by_id_validated(product_external_key)

        image = image_generation.generate_product_image(product.data["name"])

        if isinstance(image, image_generation.ImageGenerationFailure):
            return Response(
                {"detail": "Failed to generate image."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        file_name = f"{product_external_key}.{image.format.lower()}"

        return StreamingHttpResponse(
            streaming_content=[image.image_bytes],
            content_type=image.mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"',
                "Content-Length": str(image.size),
            },
        )
