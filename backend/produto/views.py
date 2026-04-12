from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Produto
from .serializers import ProdutoSerializer

class ProdutoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'produtor'):
            return Produto.objects.filter(produtor=user.produtor)

        return Produto.objects.none()