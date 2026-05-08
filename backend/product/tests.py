from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from producer.models import Producer
from product.models import Product
from retailer.models import Retailer

User = get_user_model()


class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/products/'

        self.category = Category.objects.create(name='Vegetables')
        self.other_category = Category.objects.create(name='Fruit')

        self.producer_user = User.objects.create_user(
            email='producer@example.com',
            name='Producer One',
            password='SecurePass123',
            user_type='PRODUCER'
        )
        self.producer = Producer.objects.create(
            user=self.producer_user,
            document_type='CPF',
            document_number='12345678901'
        )

        self.other_producer_user = User.objects.create_user(
            email='producer2@example.com',
            name='Producer Two',
            password='SecurePass123',
            user_type='PRODUCER'
        )
        self.other_producer = Producer.objects.create(
            user=self.other_producer_user,
            document_type='CPF',
            document_number='98765432101'
        )

        self.retailer_user = User.objects.create_user(
            email='retailer@example.com',
            name='Retailer One',
            password='SecurePass123',
            user_type='RETAILER'
        )
        self.retailer = Retailer.objects.create(
            user=self.retailer_user,
            document_type='CNPJ',
            document_number='12345678901234'
        )

        self.product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Green Lettuce',
            description='Fresh lettuce',
            total_quantity=100,
            reserved_quantity=10,
            price=12.50,
            is_active=True
        )
        self.inactive_product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Inactive Lettuce',
            total_quantity=50,
            reserved_quantity=0,
            price=8.00,
            is_active=False
        )
        self.other_product = Product.objects.create(
            category=self.other_category,
            producer=self.other_producer,
            name='Red Apple',
            total_quantity=80,
            reserved_quantity=0,
            price=20.00,
            is_active=True
        )

    def product_payload(self, **overrides):
        payload = {
            'category': self.category.id,
            'name': 'Organic Tomato',
            'description': 'Fresh tomato',
            'total_quantity': 40,
            'reserved_quantity': 0,
            'price': '9.90',
            'is_active': True
        }
        payload.update(overrides)
        return payload

    def test_producer_can_create_product_for_self(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(producer=self.other_producer.user.id)
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['producer'], self.producer.user.id)

        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.producer, self.producer)

    def test_retailer_cannot_create_product(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.post(self.url, self.product_payload())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authentication_is_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retailer_lists_only_active_products(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        product_ids = {item['id'] for item in response.data['results']}
        self.assertEqual(product_ids, {self.product.id, self.other_product.id})

    def test_producer_lists_only_own_products(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        product_ids = {item['id'] for item in response.data['results']}
        self.assertEqual(product_ids, {self.product.id, self.inactive_product.id})

    def test_producer_cannot_update_product_from_another_producer(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.patch(
            f'{self.url}{self.other_product.id}/',
            {'price': '5.00'}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_producer_can_update_own_product(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.patch(
            f'{self.url}{self.product.id}/',
            {'price': '15.00', 'name': 'Premium Lettuce'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['price'], '15.00')
        self.assertEqual(response.data['name'], 'Premium Lettuce')

    def test_retailer_can_filter_active_products(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(
            self.url,
            {
                'name': 'red apple',
                'price_min': '10',
                'price_max': '25',
                'category': self.other_category.id,
                'producer': self.other_producer.user.id,
                'ordering': 'price'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual([item['id'] for item in response.data['results']], [self.other_product.id])

    def test_total_quantity_must_be_positive(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(total_quantity=0)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('total_quantity', response.data)

    def test_reserved_quantity_cannot_be_negative(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(reserved_quantity=-1)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reserved_quantity', response.data)

    def test_reserved_quantity_cannot_exceed_total_quantity(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(total_quantity=5, reserved_quantity=6)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_partial_update_cannot_make_reserved_greater_than_total(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.patch(
            f'{self.url}{self.product.id}/',
            {'total_quantity': 5}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_price_must_be_positive(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(price='0.00')
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_available_quantity_uses_total_minus_reserved(self):
        self.assertEqual(self.product.available_quantity, 90)
