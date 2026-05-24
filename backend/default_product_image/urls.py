from django.urls import path

from default_product_image.views import (
    DefaultProductImageListView,
    DefaultProductImageUploadView,
    DefaultProductImageGenerateView,
)

urlpatterns = [
    path("", DefaultProductImageListView.as_view(), name="default-product-image-list"),
    path(
        "<str:product_external_key>/image/",
        DefaultProductImageUploadView.as_view(),
        name="default-product-image-upload",
    ),
    path(
        "<str:product_external_key>/generate-image/",
        DefaultProductImageGenerateView.as_view(),
        name="default-product-image-generate",
    ),
]
