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


from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()


class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "E-mail é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        exists = User.objects.filter(email=email).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)


class CheckDocumentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        document = request.data.get("documento")
        if not document:
            return Response({"detail": "Documento é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        clean_doc = "".join(filter(str.isdigit, str(document)))

        from producer.models import Producer
        from retailer.models import Retailer

        producer_exists = Producer.objects.filter(document_number=clean_doc).exists()
        retailer_exists = Retailer.objects.filter(document_number=clean_doc).exists()

        exists = producer_exists or retailer_exists
        return Response({"exists": exists}, status=status.HTTP_200_OK)
