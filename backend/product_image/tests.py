from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from image.models import Image
from producer.models import Producer
from product.models import Product
from product_image.models import ProductImage
from retailer.models import Retailer

User = get_user_model()


class ProductImageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Vegetables")

        self.producer_user = User.objects.create_user(
            email="producer@example.com",
            name="Producer One",
            password="SecurePass123",
            user_type="PRODUCER",
        )
        self.producer = Producer.objects.create(
            user=self.producer_user,
            document_type="CPF",
            document_number="12345678901",
        )

        self.other_producer_user = User.objects.create_user(
            email="producer2@example.com",
            name="Producer Two",
            password="SecurePass123",
            user_type="PRODUCER",
        )
        self.other_producer = Producer.objects.create(
            user=self.other_producer_user,
            document_type="CPF",
            document_number="98765432101",
        )

        self.retailer_user = User.objects.create_user(
            email="retailer@example.com",
            name="Retailer One",
            password="SecurePass123",
            user_type="RETAILER",
        )
        self.retailer = Retailer.objects.create(
            user=self.retailer_user,
            document_type="CNPJ",
            document_number="12345678901234",
        )

        self.product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name="Green Lettuce",
            description="Fresh lettuce",
            total_quantity=100,
            reserved_quantity=10,
            price=12.50,
            is_active=True,
        )
        self.other_product = Product.objects.create(
            category=self.category,
            producer=self.other_producer,
            name="Red Apple",
            total_quantity=80,
            reserved_quantity=0,
            price=20.00,
            is_active=True,
        )

    def test_producer_can_upload_product_image(self):
        self.client.force_authenticate(user=self.producer_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        response = self.client.post(
            f"/api/products/{self.product.id}/images/",
            {"image": upload},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProductImage.objects.filter(product=self.product).exists())
        self.assertIn("image", response.data)

    def test_producer_cannot_upload_to_other_product(self):
        self.client.force_authenticate(user=self.producer_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        response = self.client.post(
            f"/api/products/{self.other_product.id}/images/",
            {"image": upload},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retailer_can_list_product_images(self):
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")
        ProductImage.objects.create(product=self.product, image=image)
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(f"/api/products/{self.product.id}/images/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("image", response.data[0])

    def test_retailer_cannot_upload_product_image(self):
        self.client.force_authenticate(user=self.retailer_user)
        upload = SimpleUploadedFile(
            "image.png", b"image-data", content_type="image/png"
        )

        response = self.client.post(
            f"/api/products/{self.product.id}/images/",
            {"image": upload},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_producer_can_delete_product_image(self):
        self.client.force_authenticate(user=self.producer_user)
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")
        product_image = ProductImage.objects.create(product=self.product, image=image)

        response = self.client.delete(
            f"/api/products/{self.product.id}/images/{product_image.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductImage.objects.filter(id=product_image.id).exists())
        self.assertFalse(Image.objects.filter(id=image.id).exists())
