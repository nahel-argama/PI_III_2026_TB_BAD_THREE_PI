from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from default_product_image import image_generation
from default_product_image.models import DefaultProductImage
from image.models import Image
from product.price_scrapper_client import ExternalServiceResponse

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

    @patch("default_product_image.views.product_client.get_product_by_id_validated")
    def test_upload_for_an_existent_default_image_entry(self, mocked_get_product):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                "id": "external-3",
                "name": "External Three From Service",
                "created_at": "2024-01-01T00:00:00Z",
            },
        )
        self.client.force_authenticate(user=self.admin_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        DefaultProductImage.objects.create(
            product_external_key="external-3",
            product_name="External Three From Service",
            image=None,
        )

        response = self.client.post(
            "/api/default-product-images/external-3/image/",
            {"image": upload},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            DefaultProductImage.objects.filter(
                product_external_key="external-3"
            ).exists()
        )
        mapping = DefaultProductImage.objects.get(product_external_key="external-3")
        self.assertEqual(mapping.product_name, "External Three From Service")
        self.assertIsNotNone(mapping.image)
        self.assertEqual(mapping.image.mime_type, "image/png")

    @patch("default_product_image.views.product_client.get_product_by_id_validated")
    def test_upload_for_a_non_existent_default_image_entry(self, mocked_get_product):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                "id": "external-4",
                "name": "External Four From Service",
                "created_at": "2024-01-01T00:00:00Z",
            },
        )
        self.client.force_authenticate(user=self.admin_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        response = self.client.post(
            "/api/default-product-images/external-4/image/",
            {"image": upload},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            DefaultProductImage.objects.filter(
                product_external_key="external-4"
            ).exists()
        )
        mapping = DefaultProductImage.objects.get(product_external_key="external-4")
        self.assertEqual(mapping.product_name, "External Four From Service")
        self.assertIsNotNone(mapping.image)
        self.assertEqual(mapping.image.mime_type, "image/png")

    def test_generate_image_requires_admin(self):
        self.client.force_authenticate(user=self.non_admin_user)

        response = self.client.get(
            "/api/default-product-images/external-5/generate-image/"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "default_product_image.views.settings.ENABLE_DEFAULT_IMAGE_GENERATION",
        False,
    )
    def test_fail_to_generate_image_when_disabled(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            "/api/default-product-images/external-5/generate-image/"
        )

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("default_product_image.views.image_generation.generate_product_image")
    @patch("default_product_image.views.product_client.get_product_by_id_validated")
    @patch(
        "default_product_image.views.settings.ENABLE_DEFAULT_IMAGE_GENERATION",
        True,
    )
    def test_fail_to_generate_image_due_to_generation_failure(
        self, mocked_get_product, mocked_generate_image
    ):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                "id": "external-6",
                "name": "External Six From Service",
                "created_at": "2024-01-01T00:00:00Z",
            },
        )

        mocked_generate_image.return_value = image_generation.ImageGenerationFailure()

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            "/api/default-product-images/external-6/generate-image/"
        )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("default_product_image.views.product_client.get_product_by_id_validated")
    @patch("default_product_image.views.image_generation.generate_product_image")
    def test_generate_image_successfully(
        self, mocked_generate_image, mocked_get_product
    ):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                "id": "external-7",
                "name": "External Seven From Service",
                "created_at": "2024-01-01T00:00:00Z",
            },
        )

        image_bytes = b"generated-image-data"

        mocked_generate_image.return_value = image_generation.ImageGenerationSuccess(
            image_bytes=image_bytes,
            format="PNG",
            mime_type="image/png",
            size=len(image_bytes),
        )

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            "/api/default-product-images/external-7/generate-image/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(b"".join(response.streaming_content), image_bytes)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="external-7.png"',
        )
        self.assertEqual(response["Content-Length"], str(len(image_bytes)))
