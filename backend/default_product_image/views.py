from rest_framework import exceptions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from product import price_scrapper_client
from product.price_scrapper_client import ExternalServiceError
from default_product_image.models import DefaultProductImage
from default_product_image.serializers import (
    DefaultProductImageSerializer,
    DefaultProductImageUploadSerializer,
)
from image.models import Image
from default_product_image.filters import DefaultProductImageFilter


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
        external_response = self.get_product_by_external_key(product_external_key)
        product_name = external_response["name"]

        default_image = self.store_new_image(product_name, product_external_key, upload)

        response_serializer = DefaultProductImageSerializer(
            default_image, context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def store_new_image(self, product_name, product_external_key, upload):
        with transaction.atomic():
            default_image, was_created = DefaultProductImage.objects.get_or_create(
                product_external_key=product_external_key,
                defaults={"product_name": product_name}
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

    def get_product_by_external_key(self, product_external_key):
        response = price_scrapper_client.get_product_by_id(product_external_key)

        if isinstance(response, ExternalServiceError):
            raise exceptions.APIException(
                detail=response.message, code=status.HTTP_502_BAD_GATEWAY
            )

        if response.status != 200:
            raise exceptions.APIException(
                detail="Failed to retrieve product information from external service.",
                code=status.HTTP_502_BAD_GATEWAY,
            )

        return response.data
