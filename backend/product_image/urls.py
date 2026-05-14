from django.urls import path

from product_image.views import ProductImageListCreateView

urlpatterns = [
    path(
        "<int:product_id>/images/",
        ProductImageListCreateView.as_view(),
        name="product-image-list-create",
    ),
]
