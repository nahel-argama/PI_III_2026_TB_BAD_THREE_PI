import django_filters
from django.db.models import Q
from .models import WishlistItem


class WishlistItemFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = WishlistItem
        fields = []

    def filter_search(self, queryset, name, value):
        words = value.split()

        for word in words:
            queryset = queryset.filter(Q(product_name__icontains=word))

        return queryset
