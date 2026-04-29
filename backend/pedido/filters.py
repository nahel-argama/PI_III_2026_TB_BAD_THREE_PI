import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    
    criado_em = django_filters.DateFromToRangeFilter()

    valor_min = django_filters.NumberFilter(field_name="valor_total", lookup_expr='gte')
    valor_max = django_filters.NumberFilter(field_name="valor_total", lookup_expr='lte')

    class Meta:
        model = Pedido
        fields = []