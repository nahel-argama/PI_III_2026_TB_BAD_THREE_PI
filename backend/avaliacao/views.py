from rest_framework import viewsets, mixins
from .serializers import AvaliacaoSerializer

class AvaliacaoViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'produtor'):
            return Avaliacao.objects.filter(id_pedido__id_produtor=self.request.user.id)

        return Avaliacao.objects.filter(id_pedido__id_varejista=self.request.user.id)