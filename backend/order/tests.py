from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from producer.models import Producer
from retailer.models import Retailer
from category.models import Category
from product.models import Product
from order.models import Order
from order_item.models import OrderItem

User = get_user_model()


class OrderSmartCartTestCase(TestCase):
    """Test cases for smart cart order management"""

    def setUp(self):
        self.client = APIClient()
        self.orders_url = '/api/orders/'

        # Create a producer
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

        # Create another producer
        self.producer_user2 = User.objects.create_user(
            email='producer2@agriculture.com',
            name='Producer Name 2',
            password='SecurePass123',
            user_type='PRODUCER'
        )

        self.producer2 = Producer.objects.create(
            user=self.producer_user2,
            document_type='CPF',
            document_number='98765432101'
        )

        # Create a retailer
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

        # Create a category
        self.category = Category.objects.create(name='Electronics')

        # Create products from producer 1
        self.product1 = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Product 1',
            total_quantity=100,
            reserved_quantity=0,
            price=10.00,
            is_active=True
        )

        self.product2 = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Product 2',
            total_quantity=100,
            reserved_quantity=0,
            price=20.00,
            is_active=True
        )

        # Create a product from producer 2
        self.product3 = Product.objects.create(
            category=self.category,
            producer=self.producer2,
            name='Product 3',
            total_quantity=100,
            reserved_quantity=0,
            price=30.00,
            is_active=True
        )

        # Inactive product
        self.product_inactive = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Inactive Product',
            total_quantity=100,
            reserved_quantity=0,
            price=50.00,
            is_active=False
        )

        # Authenticate as retailer
        self.client.force_authenticate(user=self.retailer_user)

    def test_add_item_creates_new_order(self):
        """Test that adding item creates a new order"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['status'], 'PENDING')
        self.assertEqual(response.data['producer'], self.producer.user.id)
        self.assertEqual(response.data['retailer'], self.retailer.user.id)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['quantity'], 5)
        self.assertEqual(response.data['items'][0]['unit_price'], '10.00')

    def test_add_item_to_existing_order(self):
        """Test that adding item to existing producer adds to same order"""
        # Create first order
        response1 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        order_id = response1.data['id']

        # Add another item from same producer
        response2 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product2.id,
                'quantity': 3
            }
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['id'], order_id)
        self.assertEqual(len(response2.data['items']), 2)

    def test_add_same_product_increases_quantity(self):
        """Test that adding same product increases quantity"""
        # Add product once
        self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        # Add same product again
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['quantity'], 8)

    def test_add_item_different_producer_creates_new_order(self):
        """Test that items from different producers create separate orders"""
        # Add item from producer 1
        response1 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        order1_id = response1.data['id']

        # Add item from producer 2
        response2 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product3.id,
                'quantity': 2
            }
        )

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        order2_id = response2.data['id']

        # Should be different orders
        self.assertNotEqual(order1_id, order2_id)
        self.assertEqual(response1.data['producer'], self.producer.user.id)
        self.assertEqual(response2.data['producer'], self.producer2.user.id)

    def test_add_item_after_confirm_creates_new_open_order(self):
        """Test that confirmed orders are closed and are not reused."""
        response1 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        order1_id = response1.data['id']

        confirm_response = self.client.post(
            f'{self.orders_url}{order1_id}/confirm/'
        )

        self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)
        self.assertEqual(confirm_response.data['status'], 'CONFIRMED')

        response2 = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product2.id,
                'quantity': 3
            }
        )

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, response2.data)
        self.assertNotEqual(response2.data['id'], order1_id)
        self.assertEqual(response2.data['status'], 'PENDING')
        self.assertEqual(Order.objects.filter(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING'
        ).count(), 1)

    def test_open_orders_can_exist_in_parallel_by_producer(self):
        """Test retailer can keep one open order for each producer."""
        self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product3.id,
                'quantity': 2
            }
        )

        pending_orders = Order.objects.filter(
            retailer=self.retailer,
            status='PENDING'
        )

        self.assertEqual(pending_orders.count(), 2)
        self.assertEqual(
            set(pending_orders.values_list('producer', flat=True)),
            {self.producer.user.id, self.producer2.user.id}
        )

    def test_add_item_nonexistent_product(self):
        """Test adding nonexistent product fails"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': 9999,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_add_item_inactive_product(self):
        """Test adding inactive product fails"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product_inactive.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_item_invalid_quantity(self):
        """Test adding item with invalid quantity fails"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 0
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_item_missing_product_id(self):
        """Test adding item without product_id fails"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_item_missing_quantity(self):
        """Test adding item without quantity fails"""
        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_item_requires_authentication(self):
        """Test adding item requires authentication"""
        self.client.force_authenticate(user=None)

        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_item_requires_retailer(self):
        """Test adding item requires retailer user"""
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            f'{self.orders_url}add_item/',
            {
                'product_id': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderConfirmTestCase(TestCase):
    """Test cases for confirming orders"""

    def setUp(self):
        self.client = APIClient()
        self.orders_url = '/api/orders/'

        # Create producer
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

        # Create retailer
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

        # Create category and product
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

        # Create an order with items
        self.order = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING',
            total_value=0
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,
            unit_price=10.00
        )

        self.client.force_authenticate(user=self.retailer_user)

    def test_confirm_order_success(self):
        """Test confirming an order"""
        response = self.client.post(
            f'{self.orders_url}{self.order.id}/confirm/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')

        # Verify order status in database
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'CONFIRMED')

    def test_confirm_order_without_items(self):
        """Test confirming order without items fails"""
        self.order.status = 'CONFIRMED'
        self.order.save()

        # Create an empty order
        empty_order = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING',
            total_value=0
        )

        response = self.client.post(
            f'{self.orders_url}{empty_order.id}/confirm/'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_confirm_already_confirmed_order(self):
        """Test confirming already confirmed order fails"""
        self.order.status = 'CONFIRMED'
        self.order.save()

        response = self.client.post(
            f'{self.orders_url}{self.order.id}/confirm/'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_cancel_order_success(self):
        """Test canceling an order"""
        response = self.client.post(
            f'{self.orders_url}{self.order.id}/cancel/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CANCELED')

    def test_cancel_delivered_order(self):
        """Test canceling delivered order fails"""
        self.order.status = 'DELIVERED'
        self.order.save()

        response = self.client.post(
            f'{self.orders_url}{self.order.id}/cancel/'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderListingTestCase(TestCase):
    """Test cases for listing orders"""

    def setUp(self):
        self.client = APIClient()
        self.orders_url = '/api/orders/'

        # Create producer
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

        # Create retailer
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

        # Create category and product
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

        # Create multiple orders
        self.order1 = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING',
            total_value=0
        )

        OrderItem.objects.create(
            order=self.order1,
            product=self.product,
            quantity=5,
            unit_price=10.00
        )

    def test_retailer_list_own_orders(self):
        """Test retailer can list own orders"""
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order1.id)

    def test_producer_list_orders_for_products(self):
        """Test producer can list orders for their products"""
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order1.id)
