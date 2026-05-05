from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from order.models import Order
from order_item.models import OrderItem
from producer.models import Producer
from product.models import Product
from retailer.models import Retailer

User = get_user_model()


class OrderItemSecurityTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/order-items/'

        self.producer_user = User.objects.create_user(
            email='producer@agriculture.com',
            name='Producer Name',
            password='SecurePass123',
            user_type='PRODUCER'
        )
        self.producer = Producer.objects.create(
            user=self.producer_user,
            document_type='CPF',
            document_number='12345678901'
        )

        self.retailer_user = User.objects.create_user(
            email='retailer@retail.com',
            name='Retailer Name',
            password='SecurePass123',
            user_type='RETAILER'
        )
        self.retailer = Retailer.objects.create(
            user=self.retailer_user,
            document_type='CNPJ',
            document_number='12345678901234'
        )

        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Product 1',
            total_quantity=100,
            reserved_quantity=0,
            price=10.00,
            is_active=True
        )

        self.order = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING',
            total_value=0
        )

    def test_create_order_item_ignores_client_unit_price(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.post(
            self.url,
            {
                'order': self.order.id,
                'product': self.product.id,
                'quantity': 2,
                'unit_price': '0.01'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['unit_price'], '10.00')

        order_item = OrderItem.objects.get(id=response.data['id'])
        self.assertEqual(order_item.unit_price, self.product.price)

    def test_producer_cannot_create_order_item(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.url,
            {
                'order': self.order.id,
                'product': self.product.id,
                'quantity': 2
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_item_cannot_exceed_stock(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.post(
            self.url,
            {
                'order': self.order.id,
                'product': self.product.id,
                'quantity': 101
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)
