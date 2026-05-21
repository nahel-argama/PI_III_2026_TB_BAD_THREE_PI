from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from address.models import Address
from address import nominatim_client
from address.nominatim_client import Coordinates, GeocodingError, build_address_query
from address.serializers import AddressSerializer

User = get_user_model()


class NominatimClientTestCase(TestCase):
    def test_build_address_query_uses_city_state_and_brazil(self):
        query = build_address_query(
            {
                "street": "Rua 1",
                "number": "10",
                "neighborhood": "Centro",
                "city": "Rio Claro",
                "state": "SP",
            }
        )

        self.assertEqual(query, "Rio Claro SP Brasil")

    @patch("address.nominatim_client.requests.get")
    def test_geocode_address_returns_error_when_nominatim_returns_empty_list(self, mock_get):
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status.return_value = None

        result = nominatim_client.geocode_address(
            {
                "street": "Rua 1",
                "number": "10",
                "neighborhood": "Centro",
                "city": "Rio Claro",
                "state": "SP",
            }
        )

        self.assertIsInstance(result, GeocodingError)

    @patch("address.nominatim_client.requests.get")
    def test_geocode_address_returns_error_when_response_shape_is_unexpected(self, mock_get):
        mock_get.return_value.json.return_value = {"error": "bad request"}
        mock_get.return_value.raise_for_status.return_value = None

        result = nominatim_client.geocode_address(
            {
                "street": "Rua 1",
                "number": "10",
                "neighborhood": "Centro",
                "city": "Rio Claro",
                "state": "SP",
            }
        )

        self.assertIsInstance(result, GeocodingError)


class AddressSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="retailer@example.com",
            name="Retailer",
            password="SecurePass123",
            user_type="RETAILER",
        )
        self.payload = {
            "street": "Rua 1",
            "number": "10",
            "complement": "",
            "neighborhood": "Centro",
            "city": "Rio Claro",
            "state": "SP",
            "postal_code": "13500505",
        }

    @patch("address.serializers.nominatim_client.geocode_address")
    def test_create_geocodes_address_and_saves_coordinates(self, mock_geocode):
        mock_geocode.return_value = Coordinates(
            latitude=Decimal("-22.400436"),
            longitude=Decimal("-47.561290"),
        )
        serializer = AddressSerializer(data=self.payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        address = serializer.save(user=self.user)

        mock_geocode.assert_called_once()
        self.assertEqual(address.latitude, Decimal("-22.400436"))
        self.assertEqual(address.longitude, Decimal("-47.561290"))

    @patch("address.serializers.nominatim_client.geocode_address")
    def test_create_keeps_coordinates_null_when_geocoding_fails(self, mock_geocode):
        mock_geocode.return_value = GeocodingError("Address could not be geocoded.")
        serializer = AddressSerializer(data=self.payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        address = serializer.save(user=self.user)

        self.assertIsNone(address.latitude)
        self.assertIsNone(address.longitude)

    @patch("address.serializers.nominatim_client.geocode_address")
    def test_update_geocodes_using_updated_and_existing_address_parts(self, mock_geocode):
        address = Address.objects.create(
            user=self.user,
            **self.payload,
            latitude=Decimal("-22.400436"),
            longitude=Decimal("-47.561290"),
        )
        mock_geocode.return_value = Coordinates(
            latitude=Decimal("-22.448835"),
            longitude=Decimal("-47.587712"),
        )
        serializer = AddressSerializer(
            address,
            data={"neighborhood": "Jardim Novo II"},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_address = serializer.save()

        mock_geocode.assert_called_once_with(
            {
                "street": "Rua 1",
                "number": "10",
                "neighborhood": "Jardim Novo II",
                "city": "Rio Claro",
                "state": "SP",
            }
        )
        self.assertEqual(updated_address.latitude, Decimal("-22.448835"))
        self.assertEqual(updated_address.longitude, Decimal("-47.587712"))
