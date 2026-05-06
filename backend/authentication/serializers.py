from rest_framework import serializers
from django.db import transaction
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from producer.serializers import ProducerSerializer
from retailer.serializers import RetailerSerializer
from users.models import User


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

    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    profile = serializers.DictField(write_only=True, required=True)

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
        serializer = None

        if user_type is User.USER_TYPE_PRODUCER:
            serializer = ProducerSerializer(data=profile_data, context=self.context)
        else:
            serializer = RetailerSerializer(data=profile_data, context=self.context)

        serializer.is_valid(raise_exception=True)

        data["_profile_serializer"] = serializer

        return data

    def create(self, validated_data):
        profile_serializer = validated_data.pop("_profile_serializer")

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

            profile_serializer.save(user=user)

        return user
