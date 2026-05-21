from rest_framework import serializers

from address import nominatim_client
from address.nominatim_client import GeocodingError
from .models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
            "postal_code",
            "latitude",
            "longitude",
        ]
        read_only_fields = ["latitude", "longitude"]

    def validate_latitude(self, value):
        if value is not None and not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value

    def validate_longitude(self, value):
        if value is not None and not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value

    def validate_postal_code(self, value):
        value = value.replace("-", "")

        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("Postal code must have 8 digits")

        return value

    def create(self, validated_data):
        self.set_coordinates(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        address_data = {
            "street": validated_data.get("street", instance.street),
            "number": validated_data.get("number", instance.number),
            "neighborhood": validated_data.get("neighborhood", instance.neighborhood),
            "city": validated_data.get("city", instance.city),
            "state": validated_data.get("state", instance.state),
        }
        self.set_coordinates(validated_data, address_data)
        return super().update(instance, validated_data)

    def set_coordinates(self, target_data, address_data=None):
        result = nominatim_client.geocode_address(address_data or target_data)

        if isinstance(result, GeocodingError):
            raise serializers.ValidationError({"address": result.message})

        target_data["latitude"] = result.latitude
        target_data["longitude"] = result.longitude
