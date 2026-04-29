from rest_framework import viewsets, mixins
from .serializers import ItemPedidoSerializer
from users.permissions import IsVarejista
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ItemPedidoFilter

class ItemPedidoViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = ItemPedidoSerializer
    permission_classes = [IsVarejista]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemPedidoFilter

    def get_queryset(self):
        return ItemPedido.objects.filter(id_pedido__id_varejista=self.request.user.id)
