from django.urls import path

from wishlist_item.views import WishlistItemListCreateView, WishlistItemDetailView

urlpatterns = [
    path(
        'items/',
        WishlistItemListCreateView.as_view(),
        name='wishlist-items'
    ),
    path(
        'items/<int:item_id>/',
        WishlistItemDetailView.as_view(),
        name='wishlist-item-detail'
    ),
]
