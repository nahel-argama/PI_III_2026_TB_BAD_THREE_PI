from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from varejista.models import Varejista


class VarejistaAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/varejista/"

        self.varejista_user = User.objects.create_user(
            name="Varejista",
            email="varejista@email.com",
            password="12345678",
            type="VAREJISTA"
        )

        self.produtor_user = User.objects.create_user(
            name="Produtor",
            email="produtor@email.com",
            password="12345678",
            type="PRODUTOR"
        )

    def test_create_varejista_success_cpf(self):
        self.client.force_authenticate(user=self.varejista_user)

        payload = {
            "tipo_documento": "CPF",
            "documento": "12345678901"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_varejista_success_cnpj(self):
        self.client.force_authenticate(user=self.varejista_user)

        payload = {
            "tipo_documento": "CNPJ",
            "documento": "12345678901234"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_varejista_invalid_cpf(self):
        self.client.force_authenticate(user=self.varejista_user)

        response = self.client.post(self.url, {
            "tipo_documento": "CPF",
            "documento": "123"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_varejista_invalid_cnpj(self):
        self.client.force_authenticate(user=self.varejista_user)

        response = self.client.post(self.url, {
            "tipo_documento": "CNPJ",
            "documento": "123"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_varejista_user_not_varejista(self):
        self.client.force_authenticate(user=self.produtor_user)

        response = self.client.post(self.url, {
            "tipo_documento": "CPF",
            "documento": "12345678901"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_varejista_duplicate(self):
        self.client.force_authenticate(user=self.varejista_user)

        payload = {
            "tipo_documento": "CPF",
            "documento": "12345678901"
        }

        self.client.post(self.url, payload)
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_varejista_unauthenticated(self):
        response = self.client.post(self.url, {
            "tipo_documento": "CPF",
            "documento": "12345678901"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_varejista_success(self):
        varejista = Varejista.objects.create(
            id_usuario=self.varejista_user,
            tipo_documento="CPF",
            documento="12345678901"
        )

        self.client.force_authenticate(user=self.varejista_user)

        url = f"{self.url}{self.varejista_user.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["documento"], varejista.documento)

    def test_get_varejista_without_profile(self):
        self.client.force_authenticate(user=self.varejista_user)

        url = f"{self.url}{self.varejista_user.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_varejista(self):
        Varejista.objects.create(
            id_usuario=self.varejista_user,
            tipo_documento="CPF",
            documento="12345678901"
        )

        self.client.force_authenticate(user=self.varejista_user)

        url = f"{self.url}{self.varejista_user.id}/"

        response = self.client.patch(url, {
            "tipo_documento": "CNPJ",
            "documento": "12345678901234"
        })

        self.assertEqual(response.status_code, 200)

    def test_update_requires_authentication(self):
        Varejista.objects.create(
            id_usuario=self.varejista_user,
            tipo_documento="CPF",
            documento="12345678901"
        )

        url = f"{self.url}{self.varejista_user.id}/"

        response = self.client.patch(url, {
            "documento": "11111111111"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)