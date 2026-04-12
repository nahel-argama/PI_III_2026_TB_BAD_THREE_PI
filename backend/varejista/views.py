from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Varejista
from .serializers import VarejistaSerializer

class VarejistaViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Varejista.objects.select_related('user')
    serializer_class = VarejistaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if not hasattr(user, 'varejista'):
            raise PermissionDenied("Usuário não possui perfil de varejista")
        return user.varejista

    def perform_create(self, serializer):
        user = self.request.user

        if user.type != 'VAREJISTA':
            raise PermissionDenied("Usuário não é do tipo VAREJISTA")
            
        if hasattr(user, 'varejista'):
            raise PermissionDenied("Varejista já cadastrado para este usuário")
        serializer.save(user=user)