from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer, SignUpSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
