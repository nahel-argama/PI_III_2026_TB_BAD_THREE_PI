from django.urls import path

from image.views import ImageDownloadView

urlpatterns = [
    path(
        "<int:image_id>/download/",
        ImageDownloadView.as_view(),
        name="image-download",
    ),
]
