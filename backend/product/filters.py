import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, F, FloatField, Q, Value, When
from django.db.models.expressions import Func
from django.db.models.functions import Cast
from rest_framework.exceptions import ValidationError

from .models import Product

MAX_RADIUS_KM = 500


class Geography(Func):
    output_field = FloatField()
    template = "%(expressions)s::geography"


class STMakePoint(Func):
    function = "ST_MakePoint"
    output_field = FloatField()


class STSetSRID(Func):
    function = "ST_SetSRID"
    output_field = FloatField()


class STDistance(Func):
    function = "ST_Distance"
    output_field = FloatField()


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.NumberFilter(field_name="category__id")
    producer = django_filters.NumberFilter(field_name="producer")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = []

    @property
    def qs(self):
        queryset = super().qs

        search_term = self.get_search_term()
        if search_term:
            queryset = self.apply_search(queryset, search_term)

        has_geo = self.should_order_by_distance()
        if has_geo:
            latitude, longitude = self.get_request_user_coordinates(required=False)
            radius_km = self.get_optional_radius_km()
            has_coordinates = latitude is not None and longitude is not None

            if has_coordinates:
                queryset = self.apply_geo_distance(
                    queryset, latitude, longitude, radius_km
                )
            else:
                has_geo = False

        return self.apply_default_ordering(queryset, bool(search_term), has_geo)

    def get_search_term(self):
        value = self.data.get("query")
        return value.strip() if value else ""

    def should_order_by_distance(self):
        user = getattr(self.request, "user", None)
        return getattr(user, "user_type", None) == "RETAILER"

    def get_number_param(self, name, default=None):
        value = self.data.get(name)
        if value in (None, ""):
            return default
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValidationError({name: "Must be a valid number."}) from exc

    def get_optional_radius_km(self):
        if "radius_km" not in self.data:
            return None

        radius_km = self.get_number_param("radius_km")
        if radius_km <= 0:
            raise ValidationError({"radius_km": "Must be greater than zero."})
        return min(radius_km, MAX_RADIUS_KM)

    def get_request_user_coordinates(self, required=True):
        user = getattr(self.request, "user", None)
        try:
            address = getattr(user, "address", None)
        except ObjectDoesNotExist:
            address = None

        if not address or address.latitude is None or address.longitude is None:
            if not required:
                return None, None

            raise ValidationError(
                {
                    "address": (
                        "Retailer address must have latitude and longitude "
                        "to order products by distance."
                    )
                }
            )

        return float(address.latitude), float(address.longitude)

    def apply_search(self, queryset, value):
        return queryset.filter(name__icontains=value)

    def apply_geo_distance(self, queryset, latitude, longitude, radius_km=None):
        product_point = self.build_point(
            Cast(F("producer__user__address__longitude"), FloatField()),
            Cast(F("producer__user__address__latitude"), FloatField()),
        )
        user_point = self.build_point(
            Value(longitude, output_field=FloatField()),
            Value(latitude, output_field=FloatField()),
        )

        distance_expression = STDistance(product_point, user_point) / Value(1000.0)

        queryset = queryset.annotate(
            distance_km=Case(
                When(
                    producer__user__address__latitude__isnull=False,
                    producer__user__address__longitude__isnull=False,
                    then=distance_expression,
                ),
                default=Value(None),
                output_field=FloatField(),
            ),
        )

        if radius_km is None:
            return queryset

        return queryset.filter(
            Q(distance_km__lte=radius_km) | Q(distance_km__isnull=True)
        )

    def build_point(self, longitude, latitude):
        return Geography(STSetSRID(STMakePoint(longitude, latitude), Value(4326)))

    def apply_default_ordering(self, queryset, has_search, has_geo):
        ordering = []
        if has_geo:
            ordering.append(F("distance_km").asc(nulls_last=True))
        if ordering:
            ordering.extend(["price", "id"])
            return queryset.order_by(*ordering)
        
        # se não houver ordenação geográfica, usamos a padrão
        return queryset.order_by("price", "id")
