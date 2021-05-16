from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from shop.filters import ProductFilterSet, OrderFilterSet, CollectionFilterSet, ProductCommentFilterSet
from shop.models import Product, ProductComment, Orders, Collections
from shop.serializers import ProductSerializer, ProductCommentSerializer, OrderSerializer, CollectionSerializer


class ProductsViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["retrieve", "list"]:
            return [IsAuthenticated()]

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return []


class ProductCommentsViewSet(viewsets.ModelViewSet):

    queryset = ProductComment.objects.select_related("user").all()
    serializer_class = ProductCommentSerializer
    filterset_class = ProductCommentFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["retrieve", "list", "create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        check_comment = ProductComment.objects.get(pk=kwargs["pk"])
        if check_comment.user.pk != request.user.id:
            raise ValidationError("Вы не являетесь владельцем комментарий!")
        return super(ProductCommentsViewSet, self).destroy(request, *args, **kwargs)


class OrdersViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    filterset_class = OrderFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["list", "retrieve", "create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        check_order = Orders.objects.get(pk=kwargs["pk"])
        if check_order.user.pk != request.user.pk and not request.user.is_staff:
            raise ValidationError(f"вы не являетесь владельцем заказа")

        if check_order.order_status == "process" and not request.user.is_staff:
            raise ValidationError(f"заказ уже получен и готовится вы не можете изменить её!")

        if check_order.order_status == "done" and not request.user.is_staff:
            raise ValidationError(f"заказ уже готов и вы не можете изменить её!")

        return super(OrdersViewSet, self).destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Orders.objects.prefetch_related("positions").all()
        return user.orders.prefetch_related("positions").all()


class CollectionsViewSet(viewsets.ModelViewSet):

    queryset = Collections.objects.prefetch_related("product").all()
    serializer_class = CollectionSerializer
    filterset_class = CollectionFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["retrieve", "list"]:
            return [IsAuthenticated()]

        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return []

    def destroy(self, request, *args, **kwargs):
        return super(CollectionsViewSet, self).destroy(request, *args, **kwargs)
