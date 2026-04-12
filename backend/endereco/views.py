from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Endereco
from .serializers import EnderecoSerializer


class EnderecoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = EnderecoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Endereco.objects.filter(user=self.request.user).select_related('estado')