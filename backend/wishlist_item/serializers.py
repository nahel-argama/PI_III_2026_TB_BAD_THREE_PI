from rest_framework import serializers

from wishlist_item.models import WishlistItem
from wishlist_item_image.models import WishlistItemImage


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
        wishlist_image = (
            WishlistItemImage.objects.select_related("image")
            .filter(product_external_key=obj.product_external_key)
            .first()
        )
        if not wishlist_image:
            return None
        return wishlist_image.image.url

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
