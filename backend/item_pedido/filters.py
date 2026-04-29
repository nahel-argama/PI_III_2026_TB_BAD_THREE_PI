import django_filters
from .models import ItemPedido

class ItemPedidoFilter(django_filters.FilterSet):
    pedido = django_filters.NumberFilter(field_name="pedido__id")

    quantidade_min = django_filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = django_filters.NumberFilter(field_name="quantidade", lookup_expr='lte')

    preco_min = django_filters.NumberFilter(field_name="preco_unitario", lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name="preco_unitario", lookup_expr='lte')

    class Meta:
        model = ItemPedido
        fields = []