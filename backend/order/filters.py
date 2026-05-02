import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    created_at = django_filters.DateFromToRangeFilter()

    total_min = django_filters.NumberFilter(field_name="total_value", lookup_expr='gte')
    total_max = django_filters.NumberFilter(field_name="total_value", lookup_expr='lte')

    class Meta:
        model = Order
        fields = []