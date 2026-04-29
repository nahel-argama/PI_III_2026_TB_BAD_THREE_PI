from rest_framework import serializers
from users.permissions import IsRetailer
from wishlist_item_image.models import WishlistItemImage
from .models import WishlistItem
from product.price_scrapper_client import (
    ExternalServiceError,
    get_product_by_id,
)


class WishlistItemSerializer(serializers.ModelSerializer):
    product_external_key = serializers.CharField(required=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product_external_key",
            "product_name",
            "image_url",
        ]

    def get_image_url(self, obj):
        image_url = getattr(obj, "image_url", None)
        if image_url is not None:
            return image_url

        mapping = (
            WishlistItemImage.objects.select_related("image")
            .filter(product_external_key=obj.product_external_key)
            .first()
        )
        if not mapping:
            return None

        return mapping.image.url

    def create(self, validated_data):
        product_external_key = validated_data.get("product_external_key")
        result = get_product_by_id(product_external_key)

        if isinstance(result, ExternalServiceError):
            raise serializers.ValidationError("Invalid product_external_key")

        wishlist = self.context.get("wishlist")
        if wishlist is None:
            raise serializers.ValidationError("Wishlist not available")

        request = self.context.get("request")
        if not request or not IsRetailer().has_permission(request, None):
            raise serializers.ValidationError("Retailer not available")

        if wishlist.retailer_id != request.user.retailer_id:
            raise serializers.ValidationError("Retailer does not own this wishlist")

        return WishlistItem.objects.create(
            wishlist=wishlist,
            product_external_key=product_external_key,
            product_name=result.data["name"],
        )
