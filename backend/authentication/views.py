from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer
from rest_framework.permissions import AllowAny

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]