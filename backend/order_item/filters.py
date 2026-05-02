import django_filters
from .models import OrderItem

class OrderItemFilter(django_filters.FilterSet):
    order = django_filters.NumberFilter(field_name="order__id")

    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr='gte')
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr='lte')

    price_min = django_filters.NumberFilter(field_name="unit_price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="unit_price", lookup_expr='lte')

    class Meta:
        model = OrderItem
        fields = []