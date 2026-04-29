import django_filters
from .models import Produto
from django.db.models import Q

class ProdutoFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name="preco", lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name="preco", lookup_expr='lte')
    categoria = django_filters.NumberFilter(field_name="categoria__id")
    produtor = django_filters.NumberFilter(field_name="produtor__id")
    ativo = django_filters.BooleanFilter()
    nome = django_filters.CharFilter(method='filtrar_nome')

    class Meta:
        model = Produto
        fields = []

    def filtrar_nome(self, queryset, name, value):
        palavras = value.split()

        for palavra in palavras:
            queryset = queryset.filter(
                Q(nome__icontains=palavra)
            )

        return queryset