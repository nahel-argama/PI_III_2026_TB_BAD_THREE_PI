from rest_framework import viewsets, mixins
from .serializers import PedidoSerializer
from users.permissions import IsVarejista
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PedidoFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from item_pedido.serializers import ItemPedidoSerializer

class PedidoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PedidoSerializer
    permission_classes = [IsVarejista]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PedidoFilter

    @action(detail=True, methods=['get'])
    def itens(self, request, pk=None):
        pedido = self.get_object()

        itens = pedido.itens.all()
        serializer = ItemPedidoSerializer(itens, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        return Pedido.objects.filter(id_varejista=self.request.user.id)