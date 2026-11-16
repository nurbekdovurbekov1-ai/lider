import django_filters
from django.db.models import Q
from ..models import Product, Order


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    quality = django_filters.CharFilter(field_name="quality", lookup_expr="exact")
    brand = django_filters.CharFilter(field_name="brand", lookup_expr="iexact")
    car = django_filters.CharFilter(field_name="car_models__slug", lookup_expr="exact", distinct=True)
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    badge = django_filters.CharFilter(field_name="badge", lookup_expr="exact")
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    search = django_filters.CharFilter(method="filter_search")
    stock_status = django_filters.CharFilter(method="filter_stock_status")

    class Meta:
        model = Product
        fields = ["category", "quality", "brand", "car", "status", "badge", "is_active"]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(brand__icontains=value) | Q(article__icontains=value)
        )

    def filter_stock_status(self, queryset, name, value):
        low = Product.LOW_STOCK_THRESHOLD
        if value == "out":
            return queryset.filter(stock=0)
        if value == "low":
            return queryset.filter(stock__gt=0, stock__lte=low)
        if value == "ok":
            return queryset.filter(stock__gt=low)
        return queryset


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    date_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Order
        fields = ["status"]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(order_number__icontains=value)
            | Q(user__full_name__icontains=value)
            | Q(user__phone_number__icontains=value)
        )
