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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsProdutor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Produtor.objects.filter(user=self.request.user)
        return Produtor.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)