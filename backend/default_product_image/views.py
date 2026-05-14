from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

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

        default_image = self.store_new_image(product_external_key, upload)

        response_serializer = DefaultProductImageSerializer(
            default_image, context={"request": request}
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def store_new_image(self, product_external_key, upload):
        with transaction.atomic():
            default_image = DefaultProductImage.objects.filter(
                product_external_key=product_external_key,
            ).first()

            image = Image.objects.create(
                blob=upload.read(),
                mime_type=upload.content_type or "application/octet-stream",
            )

            old_image = default_image.image
            default_image.image = image
            default_image.save(update_fields=["image", "product_name"])

            if not old_image:
                return

            if old_image.default_product_images.exists():
                return

            if old_image.product_images.exists():
                return

            old_image.delete()
