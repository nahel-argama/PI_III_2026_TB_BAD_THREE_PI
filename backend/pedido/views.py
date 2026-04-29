from rest_framework import viewsets, mixins
from .serializers import PedidoSerializer
from users.permissions import IsVarejista

class PedidoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PedidoSerializer
    permission_classes = [IsVarejista]

    def get_queryset(self):
        return Pedido.objects.filter(id_varejista=self.request.user.id)