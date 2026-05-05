from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from producer.models import Producer
from retailer.models import Retailer

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Test cases for user registration endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'

    def test_register_producer_success(self):
        """Test successful producer registration"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901',
            'trade_name': 'Agrícola Silva'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], payload['email'])
        self.assertEqual(response.data['user_type'], 'PRODUCER')
        self.assertIsNotNone(response.data['producer'])
        self.assertEqual(response.data['producer']['document_number'], '12345678901')

    def test_register_retailer_success(self):
        """Test successful retailer registration"""
        payload = {
            'name': 'Loja do João',
            'email': 'loja@retail.com',
            'password': 'SecurePass123',
            'user_type': 'RETAILER',
            'document_type': 'CNPJ',
            'document_number': '12345678901234',
            'trade_name': 'Loja do João LTDA'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], payload['email'])
        self.assertEqual(response.data['user_type'], 'RETAILER')
        self.assertIsNotNone(response.data['retailer'])
        self.assertEqual(response.data['retailer']['document_number'], '12345678901234')

    def test_register_producer_creates_producer_profile(self):
        """Test that registration creates a Producer profile"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901',
            'trade_name': 'Agrícola Silva'
        }

        response = self.client.post(self.register_url, payload)
        user = User.objects.get(email=payload['email'])

        self.assertTrue(hasattr(user, 'producer'))
        self.assertEqual(user.producer.document_number, '12345678901')
        self.assertEqual(user.producer.trade_name, 'Agrícola Silva')

    def test_register_retailer_creates_retailer_profile(self):
        """Test that registration creates a Retailer profile"""
        payload = {
            'name': 'Loja do João',
            'email': 'loja@retail.com',
            'password': 'SecurePass123',
            'user_type': 'RETAILER',
            'document_type': 'CNPJ',
            'document_number': '12345678901234',
            'trade_name': 'Loja do João LTDA'
        }

        response = self.client.post(self.register_url, payload)
        user = User.objects.get(email=payload['email'])

        self.assertTrue(hasattr(user, 'retailer'))
        self.assertEqual(user.retailer.document_number, '12345678901234')
        self.assertEqual(user.retailer.trade_name, 'Loja do João LTDA')

    def test_register_without_user_type(self):
        """Test registration fails without user_type"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_invalid_user_type(self):
        """Test registration fails with invalid user_type"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'INVALID',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        self.client.post(self.register_url, payload)
        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_duplicate_document_number(self):
        """Test registration fails with duplicate document_number"""
        payload1 = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        payload2 = {
            'name': 'Maria Silva',
            'email': 'maria@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        self.client.post(self.register_url, payload1)
        response = self.client.post(self.register_url, payload2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('document_number', response.data)

    def test_register_password_too_short(self):
        """Test registration fails with password less than 8 characters"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'short',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_cpf_wrong_length(self):
        """Test registration fails with CPF wrong length"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '123456789'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('document_number', response.data)

    def test_register_cnpj_wrong_length(self):
        """Test registration fails with CNPJ wrong length"""
        payload = {
            'name': 'Loja do João',
            'email': 'loja@retail.com',
            'password': 'SecurePass123',
            'user_type': 'RETAILER',
            'document_type': 'CNPJ',
            'document_number': '123456789'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('document_number', response.data)

    def test_register_document_with_non_digits(self):
        """Test registration fails with non-digit document"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '123456789AB'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_required_fields(self):
        """Test registration fails without required fields"""
        payload = {
            'name': 'João Silva',
            'user_type': 'PRODUCER'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_trade_name_optional(self):
        """Test registration succeeds without trade_name"""
        payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginTestCase(TestCase):
    """Test cases for user login"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        self.register_url = '/api/auth/register/'

        # Create a test user
        self.user_payload = {
            'name': 'João Silva',
            'email': 'joao@agriculture.com',
            'password': 'SecurePass123',
            'user_type': 'PRODUCER',
            'document_type': 'CPF',
            'document_number': '12345678901'
        }

        self.client.post(self.register_url, self.user_payload)

    def test_login_success(self):
        """Test successful login"""
        payload = {
            'email': self.user_payload['email'],
            'password': self.user_payload['password']
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        """Test login fails with wrong password"""
        payload = {
            'email': self.user_payload['email'],
            'password': 'WrongPassword123'
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_email(self):
        """Test login fails with nonexistent email"""
        payload = {
            'email': 'nonexistent@agriculture.com',
            'password': self.user_payload['password']
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_email(self):
        """Test login fails without email"""
        payload = {
            'password': self.user_payload['password']
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_password(self):
        """Test login fails without password"""
        payload = {
            'email': self.user_payload['email']
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_token_contains_user_info(self):
        """Test that login token contains user_type and email"""
        payload = {
            'email': self.user_payload['email'],
            'password': self.user_payload['password']
        }

        response = self.client.post(self.login_url, payload)

        # Decode the access token to verify it contains user info
        from rest_framework_simplejwt.tokens import AccessToken

        token = AccessToken(response.data['access'])
        self.assertEqual(token['email'], self.user_payload['email'])
        self.assertEqual(token['user_type'], 'PRODUCER')

    def test_login_after_registration(self):
        """Test that newly registered user can login immediately"""
        new_user_payload = {
            'name': 'Maria Silva',
            'email': 'maria@agriculture.com',
            'password': 'AnotherPass456',
            'user_type': 'RETAILER',
            'document_type': 'CNPJ',
            'document_number': '12345678901234'
        }

        self.client.post(self.register_url, new_user_payload)

        login_payload = {
            'email': new_user_payload['email'],
            'password': new_user_payload['password']
        }

        response = self.client.post(self.login_url, login_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
