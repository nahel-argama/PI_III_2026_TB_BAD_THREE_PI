from django.urls import reverse
from rest_framework import serializers

from default_product_image.models import DefaultProductImage
from wishlist_item.models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product_external_key",
            "product_name",
            "image_url",
        ]
        read_only_fields = ["id", "product_name", "image_url"]

    def get_image_url(self, obj):
        default_image = (
            DefaultProductImage.objects.select_related("image")
            .filter(product_external_key=obj.product_external_key)
            .first()
        )

        if not default_image or not default_image.image_id:
            return None

        request = self.context.get("request")

        url = reverse("image-download", args=[default_image.image_id])

        if request:
            return request.build_absolute_uri(url)

        return url

    def validate_product_external_key(self, value):
        wishlist = self.context.get("wishlist")

        if not wishlist:
            raise serializers.ValidationError("Wishlist not found.")

        exists = WishlistItem.objects.filter(
            wishlist=wishlist, product_external_key=value
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "Wishlist item with this external key already exists."
            )

        return value

    def create(self, validated_data):
        wishlist = self.context.get("wishlist")
        return WishlistItem.objects.create(wishlist=wishlist, **validated_data)
