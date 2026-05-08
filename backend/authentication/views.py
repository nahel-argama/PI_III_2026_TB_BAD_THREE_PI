from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer, SignUpSerializer, MeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_data = serializer.validated_data
        response_data = {
            "refresh": token_data["refresh"],
            "access": token_data["access"],
            "user": MeSerializer(serializer.user).data,
        }

        return Response(response_data, status=200)


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = CustomTokenSerializer.get_token(user)

        response_data = {
            "refresh": str(token),
            "access": str(token.access_token),
            "user": MeSerializer(user).data,
        }

        return Response(response_data, status=201)


class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)

        data = serializer.data

        return Response(data)
