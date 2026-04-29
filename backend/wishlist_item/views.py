from django.db.models import OuterRef, Subquery
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsRetailer
from wishlist.models import Wishlist
from wishlist_item_image.models import WishlistItemImage
from .filters import WishlistItemFilter
from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistItemViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsRetailer]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WishlistItemFilter

    def get_permissions(self):
        return [IsRetailer()]

    def get_queryset(self):
        user = self.request.user

        wishlist = Wishlist.objects.filter(retailer=user.retailer).first()
        if not wishlist:
            return WishlistItem.objects.none()

        image_url_subquery = WishlistItemImage.objects.filter(
            product_external_key=OuterRef("product_external_key")
        ).values("image__url")[:1]

        return (
            WishlistItem.objects.filter(wishlist=wishlist)
            .annotate(image_url=Subquery(image_url_subquery))
            .select_related("wishlist")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user

        wishlist, _ = Wishlist.objects.get_or_create(retailer=user.retailer)
        context["wishlist"] = wishlist

        return context
