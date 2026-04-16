from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class UserAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.register_url = "/api/users/"
        self.login_url = "/api/users/login/"

        self.user_data = {
            "name": "Usuário Teste",
            "email": "teste@email.com",
            "password": "12345678",
            "type": "PRODUTOR"
        }

    def create_user(self, **kwargs):
        data = self.user_data.copy()
        data.update(kwargs)
        return User.objects.create_user(**data)

    def test_create_user_success(self):
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertNotIn("password", response.data)

    def test_create_user_without_email(self):
        data = self.user_data.copy()
        data.pop("email")

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_duplicate_email(self):
        self.create_user()

        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        self.create_user(email="login@email.com")

        response = self.client.post(self.login_url, {
            "email": "login@email.com",
            "password": "12345678"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        self.create_user(email="login@email.com")

        response = self.client.post(self.login_url, {
            "email": "login@email.com",
            "password": "senha_errada"
        })

        self.assertEqual(response.status_code, 401)

    def test_get_user_authenticated(self):
        user = self.create_user()

        self.client.force_authenticate(user=user)

        url = f"/api/users/{user.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], user.email)

    def test_get_user_unauthenticated(self):
        user = self.create_user()

        url = f"/api/users/{user.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_update_user_name(self):
        user = self.create_user()

        self.client.force_authenticate(user=user)

        url = f"/api/users/{user.id}/"

        response = self.client.patch(url, {
            "name": "Novo Nome"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Novo Nome")

    def test_update_user_email(self):
        user = self.create_user()

        self.client.force_authenticate(user=user)

        url = f"/api/users/{user.id}/"

        response = self.client.patch(url, {
            "email": "novo@email.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "novo@email.com")

    def test_update_password(self):
        user = self.create_user(password="12345678")

        self.client.force_authenticate(user=user)

        url = f"/api/users/{user.id}/"

        response = self.client.patch(url, {
            "password": "nova_senha123"
        })

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.check_password("nova_senha123"))

    def test_update_requires_authentication(self):
        user = self.create_user()

        url = f"/api/users/{user.id}/"

        response = self.client.patch(url, {
            "name": "Sem auth"
        })

        self.assertEqual(response.status_code, 401)