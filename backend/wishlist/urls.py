from django.urls import path

from wishlist_item.views import (
    WhishlistItemDeleteView,
    WishlistItemListCreateView,
    WishlistTopProductsView,
)

urlpatterns = [
    path("top-products/", WishlistTopProductsView.as_view(), name="wishlist-top-products"),
    path("items/", WishlistItemListCreateView.as_view(), name="wishlist-items"),
    path(
        "items/<int:item_id>/",
        WhishlistItemDeleteView.as_view(),
        name="wishlist-item-delete",
    ),
]
