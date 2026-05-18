from rest_framework import serializers
from django.urls import reverse

from default_product_image.models import DefaultProductImage


class DefaultProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DefaultProductImage
        fields = [
            "id",
            "product_external_key",
            "product_name",
            "image_url",
        ]

    def get_image_url(self, obj):
        if not obj.image_id:
            return None

        request = self.context.get("request")

        url = reverse("image-download", args=[obj.image_id])

        if request:
            return request.build_absolute_uri(url)
        return url


class DefaultProductImageUploadSerializer(serializers.Serializer):
    image = serializers.FileField(write_only=True)
    product_name = serializers.CharField(max_length=255, write_only=True)
