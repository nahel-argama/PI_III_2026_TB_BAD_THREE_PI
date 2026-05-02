from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Retailer
from .serializers import RetailerSerializer
from users.permissions import IsRetailer

class RetailerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Retailer.objects.select_related('user')
    serializer_class = RetailerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsRetailer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return Retailer.objects.filter(user=self.request.user)
        return Retailer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)