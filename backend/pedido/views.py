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
    filter_backends = [DjangoFilterBackend]
    filterset_class = PedidoFilter

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsVarejista()]
        
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def itens(self, request, pk=None):
        pedido = self.get_object()
        user = request.user

        if user.type == 'VAREJISTA':
            itens = pedido.itens.all()

        elif user.type == 'PRODUTOR':
            itens = pedido.itens.filter(
                produto__produtor=user.produtor
            )

        else:
            itens = []

        serializer = ItemPedidoSerializer(itens, many=True)
        return Response(serializer.data)
        
    def get_queryset(self):
        user = self.request.user

        if user.type == 'VAREJISTA':
            return Pedido.objects.filter(varejista=user.varejista)

        if user.type == 'PRODUTOR':
            return Pedido.objects.filter(
                itens__produto__produtor=user.produtor
            ).distinct()

        return Pedido.objects.none()