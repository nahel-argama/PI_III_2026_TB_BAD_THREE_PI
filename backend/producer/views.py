from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Producer
from .serializers import ProducerSerializer
from users.permissions import IsProducer

class ProducerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Producer.objects.select_related('user')
    serializer_class = ProducerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsProducer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Producer.objects.filter(user=self.request.user)
        return Producer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)