import django_filters

from default_product_image.models import DefaultProductImage


class DefaultProductImageFilter(django_filters.FilterSet):
    missing = django_filters.BooleanFilter(method="filter_missing")
    name = django_filters.CharFilter(field_name="product_name", lookup_expr="icontains")

    class Meta:
        model = DefaultProductImage
        fields = []

    def filter_missing(self, queryset, name, value):
        if value:
            queryset = queryset.filter(image__isnull=True)
        else:
            queryset = queryset.filter(image__isnull=False)
        return queryset
