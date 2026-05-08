from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from order.models import Order
from order_item.models import OrderItem
from producer.models import Producer
from product.models import Product
from retailer.models import Retailer

User = get_user_model()


class OrderItemNestedRouteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.other_retailer_user = User.objects.create_user(
            email='retailer2@example.com',
            name='Retailer Two',
            password='SecurePass123',
            user_type='RETAILER'
        )
        self.other_retailer = Retailer.objects.create(
            user=self.other_retailer_user,
            document_type='CNPJ',
            document_number='43210987654321'
        )

        self.category = Category.objects.create(name='Vegetables')
        self.product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Green Lettuce',
            total_quantity=100,
            reserved_quantity=0,
            price='10.00',
            is_active=True
        )
        self.second_product = Product.objects.create(
            category=self.category,
            producer=self.producer,
            name='Organic Tomato',
            total_quantity=100,
            reserved_quantity=0,
            price='20.00',
            is_active=True
        )
        self.other_producer_product = Product.objects.create(
            category=self.category,
            producer=self.other_producer,
            name='Red Apple',
            total_quantity=100,
            reserved_quantity=0,
            price='30.00',
            is_active=True
        )

        self.order = Order.objects.create(
            retailer=self.retailer,
            producer=self.producer,
            status='PENDING'
        )
        self.other_order = Order.objects.create(
            retailer=self.other_retailer,
            producer=self.producer,
            status='PENDING'
        )
        self.other_order_item = OrderItem.objects.create(
            order=self.other_order,
            product=self.second_product,
            quantity=7,
            unit_price='20.00'
        )

        self.item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price='10.00'
        )

        self.client.force_authenticate(user=self.retailer_user)

    def order_items_url(self, order=None):
        order = order or self.order
        return f'/api/orders/{order.id}/items/'

    def order_item_detail_url(self, item=None, order=None):
        item = item or self.item
        return f'{self.order_items_url(order)}{item.id}/'

    def test_list_items_from_nested_order(self):
        response = self.client.get(self.order_items_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.item.id)
        self.assertEqual(response.data['results'][0]['order'], self.order.id)

    def test_create_item_on_nested_order(self):
        response = self.client.post(
            self.order_items_url(),
            {
                'product': self.second_product.id,
                'quantity': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['order'], self.order.id)
        self.assertEqual(response.data['product'], self.second_product.id)
        self.assertEqual(response.data['quantity'], 3)
        self.assertEqual(response.data['unit_price'], '20.00')

    def test_create_existing_product_increases_quantity(self):
        response = self.client.post(
            self.order_items_url(),
            {
                'product': self.product.id,
                'quantity': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 5)
        self.assertEqual(OrderItem.objects.filter(order=self.order, product=self.product).count(), 1)

    def test_put_item_on_nested_order(self):
        response = self.client.put(
            self.order_item_detail_url(),
            {
                'quantity': 6
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 6)

    def test_put_item_does_not_change_product(self):
        second_item = OrderItem.objects.create(
            order=self.order,
            product=self.second_product,
            quantity=1,
            unit_price='20.00'
        )

        response = self.client.put(
            self.order_item_detail_url(second_item),
            {
                'product': self.product.id,
                'quantity': 5
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['product'], self.second_product.id)

        second_item.refresh_from_db()
        self.assertEqual(second_item.product, self.second_product)
        self.assertEqual(second_item.quantity, 5)

    def test_patch_item_on_nested_order(self):
        response = self.client.patch(
            self.order_item_detail_url(),
            {'quantity': 4}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 4)

    def test_delete_item_on_nested_order(self):
        response = self.client.delete(self.order_item_detail_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderItem.objects.filter(id=self.item.id).exists())

    def test_item_from_another_order_is_not_available_in_nested_detail(self):
        response = self.client.get(self.order_item_detail_url(self.other_order_item))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_requires_retailer_user(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.order_items_url(),
            {
                'product': self.second_product.id,
                'quantity': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_item_with_product_from_another_producer(self):
        response = self.client.post(
            self.order_items_url(),
            {
                'product': self.other_producer_product.id,
                'quantity': 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_cannot_modify_item_from_non_pending_order(self):
        self.order.status = 'CONFIRMED'
        self.order.save()

        response = self.client.patch(
            self.order_item_detail_url(),
            {'quantity': 4}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 2)

    def test_cannot_delete_item_from_non_pending_order(self):
        self.order.status = 'CONFIRMED'
        self.order.save()

        response = self.client.delete(self.order_item_detail_url())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(OrderItem.objects.filter(id=self.item.id).exists())
