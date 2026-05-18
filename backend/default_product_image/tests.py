from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from default_product_image.models import DefaultProductImage
from image.models import Image

User = get_user_model()


class DefaultProductImageAdminTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            name="Admin User",
            password="SecurePass123",
            user_type="PRODUCER",
            is_staff=True,
        )
        self.non_admin_user = User.objects.create_user(
            email="user@example.com",
            name="Regular User",
            password="SecurePass123",
            user_type="RETAILER",
        )

    def test_list_missing_defaults(self):
        self.client.force_authenticate(user=self.admin_user)
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")

        missing = DefaultProductImage.objects.create(
            product_external_key="external-1",
            product_name="External One",
        )
        DefaultProductImage.objects.create(
            product_external_key="external-2",
            product_name="External Two",
            image=image,
        )

        response = self.client.get("/api/default-product-images/?missing=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], missing.id)

    def test_list_requires_admin(self):
        self.client.force_authenticate(user=self.non_admin_user)

        response = self.client.get("/api/default-product-images/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_for_an_existent_default_image_entry(self):
        self.client.force_authenticate(user=self.admin_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        DefaultProductImage.objects.create(
            product_external_key="external-3",
            product_name="External Three",
            image=None,
        )

        response = self.client.post(
            "/api/default-product-images/external-3/image/",
            {"image": upload, "product_name": "External Three"},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            DefaultProductImage.objects.filter(
                product_external_key="external-3"
            ).exists()
        )
        mapping = DefaultProductImage.objects.get(product_external_key="external-3")
        self.assertEqual(mapping.product_name, "External Three")
        self.assertIsNotNone(mapping.image)
        self.assertEqual(mapping.image.mime_type, "image/png")

    def test_upload_for_a_non_existent_default_image_entry(self):
        self.client.force_authenticate(user=self.admin_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        response = self.client.post(
            "/api/default-product-images/external-4/image/",
            {"image": upload, "product_name": "External Four"},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            DefaultProductImage.objects.filter(
                product_external_key="external-4"
            ).exists()
        )
        mapping = DefaultProductImage.objects.get(product_external_key="external-4")
        self.assertEqual(mapping.product_name, "External Four")
        self.assertIsNotNone(mapping.image)
        self.assertEqual(mapping.image.mime_type, "image/png")
