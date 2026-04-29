from django.urls import include, path
from rest_framework.routers import DefaultRouter
from wishlist_item.views import WishlistItemViewSet

router = DefaultRouter()
router.register(r"items", WishlistItemViewSet, basename="wishlist-item")

urlpatterns = [
    path("", include(router.urls)),
]
