from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from address.models import Address
from category.models import Category
from producer.models import Producer
from product.models import Product
from product.price_scrapper_client import ExternalServiceResponse
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
            document_number='12345678901',
            trade_name='Producer One Farm'
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
            document_number='98765432101',
            trade_name='Producer Two Farm'
        )
        Address.objects.create(
            user=self.producer_user,
            street='Farm Road',
            number='10',
            complement='',
            neighborhood='Rural',
            city='Sao Paulo',
            state='SP',
            postal_code='01001000',
            latitude=-23.550520,
            longitude=-46.633308
        )
        Address.objects.create(
            user=self.other_producer_user,
            street='Far Farm Road',
            number='20',
            complement='',
            neighborhood='Rural',
            city='Campinas',
            state='SP',
            postal_code='13010000',
            latitude=-22.905560,
            longitude=-47.060830
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
        Address.objects.create(
            user=self.retailer_user,
            street='Store Road',
            number='30',
            complement='',
            neighborhood='Centro',
            city='Sao Paulo',
            state='SP',
            postal_code='01001000',
            latitude=-23.551000,
            longitude=-46.634000
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
            'external_id': 'external-1',
            'description': 'Fresh tomato',
            'total_quantity': 40,
            'reserved_quantity': 0,
            'price': '9.90',
            'is_active': True
        }
        payload.update(overrides)
        return payload

    def external_product_response(self, name='Organic Tomato'):
        return ExternalServiceResponse(
            status=200,
            data={
                'id': 'external-1',
                'name': name,
                'created_at': '2026-05-20T00:00:00Z',
            }
        )

    @patch('product.serializers.price_scrapper_client.get_product_by_id')
    def test_producer_can_create_product_for_self(self, mock_get_product):
        mock_get_product.return_value = self.external_product_response()
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(producer=self.other_producer.user.id)
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['producer'], self.producer.id)
        self.assertEqual(response.data['name'], 'Organic Tomato')

        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.producer, self.producer)

    @patch('product.serializers.price_scrapper_client.get_product_by_id')
    def test_create_product_uses_external_id_to_store_name(self, mock_get_product):
        mock_get_product.return_value = self.external_product_response('External Tomato')
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(external_id='external-1')
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        mock_get_product.assert_called_once_with('external-1')
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.name, 'External Tomato')
        self.assertEqual(response.data['name'], 'External Tomato')

    def test_create_product_rejects_name_payload(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            self.product_payload(name='Should Not Be Accepted')
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

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

    def test_producer_lists_only_own_active_products(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        product_ids = {item['id'] for item in response.data['results']}
        self.assertEqual(product_ids, {self.product.id})

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
            {'price': '15.00'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['price'], '15.00')
        self.assertEqual(response.data['name'], 'Green Lettuce')

    @patch('product.serializers.price_scrapper_client.get_product_by_id')
    def test_update_product_uses_external_id_to_store_name(self, mock_get_product):
        mock_get_product.return_value = self.external_product_response('External Lettuce')
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.patch(
            f'{self.url}{self.product.id}/',
            {'external_id': 'external-1'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        mock_get_product.assert_called_once_with('external-1')
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'External Lettuce')
        self.assertEqual(response.data['name'], 'External Lettuce')

    def test_retailer_can_filter_active_products(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(
            self.url,
            {
                'query': 'red apple',
                'price_min': '10',
                'price_max': '25',
                'category': self.other_category.id,
                'producer': self.other_producer.id,
                'ordering': 'price'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual([item['id'] for item in response.data['results']], [self.other_product.id])

    def test_retailer_products_are_ordered_by_distance_from_address(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        results_by_id = {
            item['id']: item
            for item in response.data['results']
        }
        near_distance = results_by_id[self.product.id]['distance_km']
        far_distance = results_by_id[self.other_product.id]['distance_km']

        self.assertGreater(near_distance, 0.0)
        self.assertGreater(far_distance, near_distance)
        self.assertEqual(
            [item['id'] for item in response.data['results']],
            [self.product.id, self.other_product.id]
        )

    def test_retailer_can_filter_products_by_optional_radius(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.url, {'radius_km': '10'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.product.id)
        self.assertGreater(response.data['results'][0]['distance_km'], 0.0)

    def test_retailer_without_coordinates_can_list_products_without_radius(self):
        self.client.force_authenticate(user=self.retailer_user)
        self.retailer_user.address.latitude = None
        self.retailer_user.address.longitude = None
        self.retailer_user.address.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIsNone(response.data['results'][0]['distance_km'])

    def test_retailer_without_coordinates_can_list_products_with_radius_ignored(self):
        self.client.force_authenticate(user=self.retailer_user)
        self.retailer_user.address.latitude = None
        self.retailer_user.address.longitude = None
        self.retailer_user.address.save()

        response = self.client.get(self.url, {'radius_km': '10'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIsNone(response.data['results'][0]['distance_km'])

    def test_retailer_radius_keeps_products_without_producer_coordinates(self):
        producer_without_address_user = User.objects.create_user(
            email='producer3@example.com',
            name='Producer Three',
            password='SecurePass123',
            user_type='PRODUCER'
        )
        producer_without_address = Producer.objects.create(
            user=producer_without_address_user,
            document_type='CPF',
            document_number='11122233344',
            trade_name='Producer Three Farm'
        )
        product_without_distance = Product.objects.create(
            category=self.category,
            producer=producer_without_address,
            name='Unknown Distance Product',
            total_quantity=50,
            reserved_quantity=0,
            price=30.00,
            is_active=True
        )
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.url, {'radius_km': '10'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(
            [item['id'] for item in response.data['results']],
            [self.product.id, product_without_distance.id]
        )
        self.assertIsNone(response.data['results'][1]['distance_km'])

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
