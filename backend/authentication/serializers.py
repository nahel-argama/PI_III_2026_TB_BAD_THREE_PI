from rest_framework import serializers
from django.db import transaction
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from producer.serializers import ProducerSerializer
from retailer.serializers import RetailerSerializer
from users.models import User
from address.serializers import AddressSerializer


class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["user_type"] = user.user_type

        return token


class SignUpSerializer(serializers.Serializer):
    producer_type = User.USER_TYPE_CHOICES
    profile_serializer = None
    address_serializer = None

    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    profile = serializers.DictField(write_only=True, required=True)
    address = serializers.DictField(write_only=True, required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_document_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Document must contain only numbers.")
        return value

    def validate(self, data):
        user_type = data["user_type"]
        profile_data = data["profile"]
        address_data = data["address"]
        errors = {}

        if user_type is User.USER_TYPE_PRODUCER:
            self.profile_serializer = ProducerSerializer(
                data=profile_data, context=self.context
            )
        else:
            self.profile_serializer = RetailerSerializer(
                data=profile_data, context=self.context
            )

        if not self.profile_serializer.is_valid():
            errors["profile"] = self.profile_serializer.errors

        self.address_serializer = AddressSerializer(
            data=address_data, context=self.context
        )

        if not self.address_serializer.is_valid():
            errors["address"] = self.address_serializer.errors

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        name = validated_data.pop("name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user_type = validated_data.pop("user_type")

        with transaction.atomic():
            user = User.objects.create_user(
                password=password,
                name=name,
                email=email,
                user_type=user_type,
            )

            self.profile_serializer.save(user=user)

            self.address_serializer.save(user=user)

        return user


class MeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "user_type", "profile", "address"]

    def get_profile(self, obj):
        if obj.user_type == User.USER_TYPE_PRODUCER:
            return ProducerSerializer(obj.producer).data
        elif obj.user_type == User.USER_TYPE_RETAILER:
            return RetailerSerializer(obj.retailer).data
        return None

    def get_address(self, obj):
        address = getattr(obj, "address", None)
        if not address:
            return None
        return AddressSerializer(address).data
