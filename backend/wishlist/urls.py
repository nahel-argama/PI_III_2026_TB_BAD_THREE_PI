from django.urls import path

from wishlist_item.views import WishlistItemListCreateView, WhishlistItemDeleteView

urlpatterns = [
    path("items/", WishlistItemListCreateView.as_view(), name="wishlist-items"),
    path(
        "items/<int:item_id>/",
        WhishlistItemDeleteView.as_view(),
        name="wishlist-item-delete",
    ),
]
