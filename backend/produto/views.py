from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Produto
from .serializers import ProdutoSerializer
from users.permissions import IsProdutor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ProdutoFilter

class ProdutoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.select_related('id_produtor', 'id_categoria')
    filterset_class = ProdutoFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['preco', 'nome']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsProdutor]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'produtor'):
            return Produto.objects.filter(id_produtor=user.produtor)

        if hasattr(user, 'varejista'):
            return Produto.objects.filter(ativo=True)
        
        return Produto.objects.none()