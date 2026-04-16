from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Produtor
from .serializers import ProdutorSerializer

class ProdutorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Produtor.objects.select_related('user')
    serializer_class = ProdutorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if not hasattr(user, 'produtor'):
            raise PermissionDenied("Usuário não possui perfil de produtor")

        return user.produtor

    def perform_create(self, serializer):
        user = self.request.user

        if user.type != 'PRODUTOR':
            raise PermissionDenied("Usuário não é do tipo PRODUTOR")

        if hasattr(user, 'produtor'):
            raise PermissionDenied("Produtor já cadastrado para este usuário")

        serializer.save(user=user)