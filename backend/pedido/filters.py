import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    
    criado_de = django_filters.DateTimeFilter(field_name="criado_em", lookup_expr='gte')
    criado_ate = django_filters.DateTimeFilter(field_name="criado_em", lookup_expr='lte')

    valor_min = django_filters.NumberFilter(field_name="valor_total", lookup_expr='gte')
    valor_max = django_filters.NumberFilter(field_name="valor_total", lookup_expr='lte')

    class Meta:
        model = Pedido
        fields = []