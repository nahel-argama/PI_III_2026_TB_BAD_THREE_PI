import django_filters
from .models import Product
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="category__id")
    producer = django_filters.NumberFilter(field_name="producer__id")
    is_active = django_filters.BooleanFilter()
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Product
        fields = []

    def filter_name(self, queryset, name, value):
        words = value.split()

        for word in words:
            queryset = queryset.filter(
                Q(name__icontains=word)
            )

        return queryset