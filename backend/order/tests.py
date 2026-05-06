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


class OrderLifecycleWithNestedItemsTestCase(TestCase):
    """Test cases for order lifecycle using only nested item routes."""

    def setUp(self):
        self.client = APIClient()
        self.orders_url = '/api/orders/'

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

        self.product3 = Product.objects.create(
            category=self.category,
            producer=self.producer2,
            name='Product 3',
            total_quantity=100,
            reserved_quantity=0,
            price=30.00,
            is_active=True
        )

        self.product_inactive = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Inactive Product',
            total_quantity=100,
            reserved_quantity=0,
            price=50.00,
            is_active=False
        )

        self.client.force_authenticate(user=self.retailer_user)

    def create_order(self, producer=None):
        producer = producer or self.producer
        return self.client.post(
            self.orders_url,
            {'producer': producer.user.id}
        )

    def order_items_url(self, order_id):
        return f'{self.orders_url}{order_id}/items/'

    def order_item_detail_url(self, order_id, item_id):
        return f'{self.order_items_url(order_id)}{item_id}/'

    def test_retailer_creates_order_then_manages_items_through_nested_routes(self):
        order_response = self.create_order()

        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED, order_response.data)
        order_id = order_response.data['id']
        self.assertEqual(order_response.data['status'], 'PENDING')
        self.assertEqual(order_response.data['retailer'], self.retailer.user.id)
        self.assertEqual(order_response.data['producer'], self.producer.user.id)
        self.assertEqual(order_response.data['items'], [])

        item_response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(item_response.status_code, status.HTTP_201_CREATED, item_response.data)
        item_id = item_response.data['id']
        self.assertEqual(item_response.data['order'], order_id)
        self.assertEqual(item_response.data['unit_price'], '10.00')

        patch_response = self.client.patch(
            self.order_item_detail_url(order_id, item_id),
            {'quantity': 3}
        )

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK, patch_response.data)
        self.assertEqual(patch_response.data['quantity'], 3)

        order_detail_response = self.client.get(f'{self.orders_url}{order_id}/')

        self.assertEqual(order_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_detail_response.data['total_value'], '30.00')
        self.assertEqual(len(order_detail_response.data['items']), 1)
        self.assertEqual(order_detail_response.data['items'][0]['quantity'], 3)

    def test_same_product_nested_post_increases_existing_item_quantity(self):
        order_id = self.create_order().data['id']

        self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 5
            }
        )
        response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['quantity'], 8)
        self.assertEqual(OrderItem.objects.filter(order_id=order_id, product=self.product1).count(), 1)

    def test_retailer_can_keep_one_pending_order_per_producer(self):
        first_response = self.create_order(self.producer)
        second_response = self.create_order(self.producer2)

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED, first_response.data)
        self.assertEqual(second_response.status_code, status.HTTP_201_CREATED, second_response.data)
        self.assertNotEqual(first_response.data['id'], second_response.data['id'])

        pending_orders = Order.objects.filter(
            retailer=self.retailer,
            status='PENDING'
        )

        self.assertEqual(pending_orders.count(), 2)
        self.assertEqual(
            set(pending_orders.values_list('producer', flat=True)),
            {self.producer.user.id, self.producer2.user.id}
        )

    def test_retailer_cannot_create_duplicate_pending_order_for_same_producer(self):
        first_response = self.create_order(self.producer)
        duplicate_response = self.create_order(self.producer)

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED, first_response.data)
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.filter(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING'
        ).count(), 1)

    def test_nested_item_create_requires_authentication(self):
        order_id = self.create_order().data['id']
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nested_item_create_requires_retailer(self):
        order_id = self.create_order().data['id']
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nested_item_create_validates_product_stock_and_producer(self):
        order_id = self.create_order().data['id']

        inactive_response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product_inactive.id,
                'quantity': 5
            }
        )
        overstock_response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 101
            }
        )
        other_producer_response = self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product3.id,
                'quantity': 1
            }
        )

        self.assertEqual(inactive_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(overstock_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(other_producer_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderItem.objects.filter(order_id=order_id).count(), 0)

    def test_direct_order_item_route_is_not_registered(self):
        response = self.client.post(
            '/api/order-items/',
            {
                'order': 1,
                'product': self.product1.id,
                'quantity': 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_can_be_confirmed_after_nested_item_create(self):
        order_id = self.create_order().data['id']
        self.client.post(
            self.order_items_url(order_id),
            {
                'product': self.product1.id,
                'quantity': 5
            }
        )

        response = self.client.post(f'{self.orders_url}{order_id}/confirm/')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['status'], 'CONFIRMED')

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.total_quantity, 95)


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

        self.product.refresh_from_db()
        self.assertEqual(self.product.total_quantity, 95)

    def test_confirm_order_fails_when_stock_is_insufficient(self):
        """Test confirming an order validates current stock before deduction."""
        self.product.total_quantity = 4
        self.product.save()

        response = self.client.post(
            f'{self.orders_url}{self.order.id}/confirm/'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        self.order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.order.status, 'PENDING')
        self.assertEqual(self.product.total_quantity, 4)

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

    def test_producer_cannot_cancel_order(self):
        """Test producer cannot cancel a retailer order."""
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            f'{self.orders_url}{self.order.id}/cancel/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        self.product2 = Product.objects.create(
            category=self.category,
            producer=self.producer2,
            name='Product 2',
            total_quantity=100,
            reserved_quantity=0,
            price=20.00,
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

        self.order2 = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer2,
            status='PENDING',
            total_value=0
        )

        OrderItem.objects.create(
            order=self.order2,
            product=self.product2,
            quantity=2,
            unit_price=20.00
        )

    def test_retailer_list_own_orders(self):
        """Test retailer can list own orders"""
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            {item['id'] for item in response.data},
            {self.order1.id, self.order2.id}
        )

    def test_retailer_can_filter_orders_by_producer(self):
        self.client.force_authenticate(user=self.retailer_user)

        response = self.client.get(
            self.orders_url,
            {
                'status': 'PENDING',
                'producer': self.producer2.user.id
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item['id'] for item in response.data], [self.order2.id])

    def test_producer_list_orders_for_products(self):
        """Test producer can list orders for their products"""
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order1.id)
