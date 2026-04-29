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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsVarejista()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Varejista.objects.filter(user=self.request.user)
        return Varejista.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)