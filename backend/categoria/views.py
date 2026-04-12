from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Categoria
from .serializers import CategoriaSerializer

class CategoriaViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]