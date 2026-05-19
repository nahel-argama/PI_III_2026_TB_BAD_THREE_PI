from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import ProductViewSet
from product_image.views import ProductImageDeleteView, ProductImageViewSet

router = DefaultRouter()
router.register(r"", ProductViewSet, basename="product")

products_router = NestedSimpleRouter(router, r"", lookup="product")
products_router.register(r"images", ProductImageViewSet, basename="product-images")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:product_id>/images/<int:image_id>/",
        ProductImageDeleteView.as_view(),
        name="product-image-delete",
    ),
    path("", include(products_router.urls)),
]
