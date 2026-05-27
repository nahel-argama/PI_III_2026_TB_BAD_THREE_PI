from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from address.models import Address
from producer.models import Producer
from retailer.models import Retailer
from wishlist.models import Wishlist
from wishlist_item.models import WishlistItem
from default_product_image.models import DefaultProductImage
from image.models import Image
from product.price_scrapper_client import ExternalServiceResponse

User = get_user_model()


class WishlistItemNestedRouteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.retailer_user = User.objects.create_user(
            email='retailer@example.com',
            name='Retailer One',
            password='SecurePass123',
            user_type='RETAILER'
        )
        self.retailer = Retailer.objects.create(
            user=self.retailer_user,
            document_type='CNPJ',
            document_number='12345678901234',
            trade_name='Retailer One Shop'
        )
        self.wishlist = Wishlist.objects.create(retailer=self.retailer)

        self.other_retailer_user = User.objects.create_user(
            email='retailer2@example.com',
            name='Retailer Two',
            password='SecurePass123',
            user_type='RETAILER'
        )
        self.other_retailer = Retailer.objects.create(
            user=self.other_retailer_user,
            document_type='CNPJ',
            document_number='43210987654321',
            trade_name='Retailer Two Shop'
        )
        self.other_wishlist = Wishlist.objects.create(retailer=self.other_retailer)

        self.producer_user = User.objects.create_user(
            email='producer@example.com',
            name='Producer One',
            password='SecurePass123',
            user_type='PRODUCER'
        )
        self.producer = Producer.objects.create(
            user=self.producer_user,
            document_type='CNPJ',
            document_number='11122233344455',
            trade_name='Producer One Farm'
        )

        self.create_address(self.retailer_user, state='SP')
        self.create_address(self.other_retailer_user, state='SP')
        self.create_address(self.producer_user, state='SP')

        self.item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            product_external_key='external-1',
            product_name='External Product One'
        )
        self.other_item = WishlistItem.objects.create(
            wishlist=self.other_wishlist,
            product_external_key='external-2',
            product_name='External Product Two'
        )

        self.client.force_authenticate(user=self.retailer_user)

    def create_address(self, user, state):
        return Address.objects.create(
            user=user,
            street='Main Street',
            number='123',
            neighborhood='Downtown',
            city='Sao Paulo',
            state=state,
            postal_code='01000-000',
        )

    def wishlist_items_url(self):
        return '/api/wishlists/items/'

    def wishlist_top_products_url(self):
        return '/api/wishlists/top-products/'

    def wishlist_item_detail_url(self, item=None):
        item = item or self.item
        return f'{self.wishlist_items_url()}{item.id}/'

    def test_list_items_for_retailer_wishlist(self):
        response = self.client.get(self.wishlist_items_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.item.id)

    def test_list_items_returns_image_url_when_available(self):
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")
        DefaultProductImage.objects.create(
            product_external_key=self.item.product_external_key,
            product_name=self.item.product_name,
            image=image,
        )

        response = self.client.get(self.wishlist_items_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_url = f"http://testserver/api/images/{image.id}/download/"
        self.assertEqual(response.data['results'][0]['image_url'], expected_url)

    def test_list_items_returns_null_image_url_when_missing(self):
        response = self.client.get(self.wishlist_items_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['results'][0]['image_url'])

    @patch('wishlist_item.views.price_scrapper_client.get_product_by_id')
    def test_create_item_on_wishlist(self, mocked_get_product):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                'id': 'external-3',
                'name': 'External Product Three',
                'created_at': '2024-01-01T00:00:00Z'
            }
        )

        response = self.client.post(
            self.wishlist_items_url(),
            {'product_external_key': 'external-3'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['product_external_key'], 'external-3')
        self.assertEqual(response.data['product_name'], 'External Product Three')
        self.assertTrue(
            WishlistItem.objects.filter(
                wishlist=self.wishlist,
                product_external_key='external-3'
            ).exists()
        )

    @patch('wishlist_item.views.price_scrapper_client.get_product_by_id')
    def test_create_item_creates_default_image_placeholder(self, mocked_get_product):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                'id': 'external-3',
                'name': 'External Product Three',
                'created_at': '2024-01-01T00:00:00Z'
            }
        )

        response = self.client.post(
            self.wishlist_items_url(),
            {'product_external_key': 'external-3'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(
            DefaultProductImage.objects.filter(
                product_external_key='external-3'
            ).exists()
        )
        default_image = DefaultProductImage.objects.get(
            product_external_key='external-3'
        )
        self.assertEqual(default_image.product_name, 'External Product Three')
        self.assertIsNone(default_image.image)

    @patch('wishlist_item.views.price_scrapper_client.get_product_by_id')
    def test_create_rejects_existing_external_key(self, mocked_get_product):
        mocked_get_product.return_value = ExternalServiceResponse(
            status=200,
            data={
                'id': self.item.product_external_key,
                'name': 'External Product One',
                'created_at': '2024-01-01T00:00:00Z'
            }
        )

        response = self.client.post(
            self.wishlist_items_url(),
            {'product_external_key': self.item.product_external_key}
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_delete_item_does_not_remove_image(self):
        image = Image.objects.create(blob=b"image-data", mime_type="image/png")
        default_image = DefaultProductImage.objects.create(
            product_external_key=self.item.product_external_key,
            product_name=self.item.product_name,
            image=image,
        )

        response = self.client.delete(self.wishlist_item_detail_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WishlistItem.objects.filter(id=self.item.id).exists())
        self.assertTrue(
            DefaultProductImage.objects.filter(id=default_image.id).exists()
        )

    def test_retailer_only_permission_for_list(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.wishlist_items_url())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retailer_only_permission_for_create(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.post(
            self.wishlist_items_url(),
            {'product_external_key': 'external-3'}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_top_products_uses_producer_state_and_default_top(self):
        self.client.force_authenticate(user=self.producer_user)
        WishlistItem.objects.create(
            wishlist=self.other_wishlist,
            product_external_key='external-1',
            product_name='External Product One'
        )
        WishlistItem.objects.create(
            wishlist=self.other_wishlist,
            product_external_key='external-3',
            product_name='External Product Three'
        )

        response = self.client.get(self.wishlist_top_products_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'SP')
        self.assertEqual(response.data['top'], 5)
        self.assertEqual(response.data['total_items'], 4)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['product_external_key'], 'external-1')
        self.assertEqual(response.data['results'][0]['total'], 2)
        self.assertEqual(response.data['results'][0]['percentage'], 50)

    def test_top_products_filters_by_query_state_and_limit(self):
        rj_user = User.objects.create_user(
            email='retailer-rj@example.com',
            name='Retailer RJ',
            password='SecurePass123',
            user_type='RETAILER'
        )
        rj_retailer = Retailer.objects.create(
            user=rj_user,
            document_type='CNPJ',
            document_number='55566677788899',
            trade_name='Retailer RJ Shop'
        )
        rj_wishlist = Wishlist.objects.create(retailer=rj_retailer)
        self.create_address(rj_user, state='RJ')
        WishlistItem.objects.create(
            wishlist=rj_wishlist,
            product_external_key='external-rj',
            product_name='External Product RJ'
        )
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(
            self.wishlist_top_products_url(),
            {'state': 'rj', 'top': 1}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'RJ')
        self.assertEqual(response.data['top'], 1)
        self.assertEqual(response.data['total_items'], 1)
        self.assertEqual(response.data['results'][0]['product_external_key'], 'external-rj')
        self.assertEqual(response.data['results'][0]['percentage'], 100)

    def test_top_products_rejects_invalid_top(self):
        self.client.force_authenticate(user=self.producer_user)

        response = self.client.get(self.wishlist_top_products_url(), {'top': 'zero'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_products_requires_producer(self):
        response = self.client.get(self.wishlist_top_products_url(), {'state': 'SP'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
