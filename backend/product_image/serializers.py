from rest_framework import serializers
from django.urls import reverse

from product_image.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "created_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")

        url = reverse("image-download", args=[obj.image_id])

        if request:
            return request.build_absolute_uri(url)

        return url


class ProductImageUploadSerializer(serializers.Serializer):
    image = serializers.FileField(write_only=True)
