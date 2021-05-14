from django_filters import rest_framework as filters

from shop.models import Orders, Product, Collections, ProductComment


class OrderFilterSet(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Orders.objects.all()
    )
    order_status = filters.CharFilter(lookup_expr="iexact")
    total_sum = filters.NumberFilter()
    created_date = filters.DateFromToRangeFilter()
    updated_date = filters.DateFromToRangeFilter()
    product_name = filters.CharFilter(
        field_name="order_position__product__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Orders
        fields = ["id", "order_status", "product_name", "created_date", "total_sum", "updated_date"]


class ProductFilterSet(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Product.objects.all()
    )
    name = filters.CharFilter(lookup_expr="iexact")
    created_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "created_date"]


class CollectionFilterSet(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter()
    product = filters.CharFilter(
        field_name="product__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Collections
        fields = ["product", "created_date"]


class ProductCommentFilterSet(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter()

    class Meta:
        model = ProductComment
        fields = ["user", "product", "created_date"]
