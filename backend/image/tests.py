from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from image.models import Image

User = get_user_model()


class ImageDownloadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="retailer@example.com",
            name="Retailer One",
            password="SecurePass123",
            user_type="RETAILER",
        )
        self.client.force_authenticate(user=self.user)

    def test_download_image_returns_blob(self):
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")

        response = self.client.get(f"/api/images/{image.id}/download/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertEqual(response.content, b"image-data")

    def test_download_missing_image_returns_404(self):
        response = self.client.get("/api/images/9999/download/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
