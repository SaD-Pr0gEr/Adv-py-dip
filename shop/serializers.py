from rest_framework import serializers

from shop.models import User, Orders, Product, ProductComment, Collections, OrderPositions, StatusChoices


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "created_date", "updated_date", "photo"]

    def create(self, validated_data):
        return super().create(validated_data)


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductComment
        fields = ["id", "user", "product", "comment", "rating", "created_date", "updated_date"]

    def create(self, validated_data):
        user = validated_data["user"]
        check_count = ProductComment.objects.filter(user=user, product=self.validated_data["product"]).count()
        if check_count >= 1:
            raise serializers.ValidationError(f"вы не можете оставить более 1 комментарий на этот продукт")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        creator = instance.user
        if creator.pk != self.context["request"].user.id:
            raise serializers.ValidationError(f"Вы не являетесь владельцем комментарий!")
        return super().update(instance, validated_data)


class OrderPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPositions
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    positions = OrderPositionSerializer(many=True)
    total_sum = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    order_status = serializers.CharField(read_only=True)

    class Meta:
        model = Orders
        fields = [
            "id", "positions", "total_sum", "order_status", "total_quantity",
            "created_date", "updated_date"
        ]

    def create(self, validated_data):
        check_positions = validated_data["positions"]
        if not check_positions:
            raise serializers.ValidationError(f"Вы ничего не передали в список позиции!")
        products = validated_data.pop("positions")

        if validated_data["user"].is_staff and "order_status" not in self.context["request"].data:
            raise serializers.ValidationError(f"Вы не передали статус заказа!")

        if validated_data["user"].is_staff and self.context["request"].data["order_status"] in ["open", "process", "done"]:
            validated_data["order_status"] = self.context["request"].data["order_status"]
        if products:
            total_sum = 0
            total_quantity = 0
            for product in products:
                total_sum += product["product"].price * product["quantity"]
                total_quantity += product["quantity"]
            validated_data["total_quantity"] = total_quantity
            validated_data["total_sum"] = total_sum
            create_order = super().create(validated_data)
            to_save = []
            for position in products:
                to_save.append(OrderPositions(
                    order=create_order,
                    product=position["product"],
                    quantity=position["quantity"]
                ))
            OrderPositions.objects.bulk_create(to_save)
            return create_order

    def update(self, instance, validated_data):
        creator = instance.user
        if creator.pk != validated_data["user"].id and not validated_data["user"].is_staff:
            raise serializers.ValidationError(f"Вы не являетесь владельцем заказа или админом!")

        if instance.order_status == "process" and not validated_data["user"].is_staff:
            raise serializers.ValidationError(f"заказ уже получен и готовится вы не можете изменить её!")

        if instance.order_status == "done" and not validated_data["user"].is_staff:
            raise serializers.ValidationError(f"заказ уже готов и вы не можете изменить её!")

        if validated_data["user"].is_staff and "order_status" not in self.context["request"].data:
            raise serializers.ValidationError(f"Вы не передали статус заказа!")

        if validated_data["user"].is_staff and self.context["request"].data["order_status"] in ["open", "process", "done"]:
            validated_data["order_status"] = self.context["request"].data["order_status"]

        products = validated_data.pop("positions")
        if products:
            total_sum = 0
            total_quantity = 0
            for product in products:
                total_sum += product["product"].price * product["quantity"]
                total_quantity += product["quantity"]
            validated_data["total_quantity"] = total_quantity
            validated_data["total_sum"] = total_sum
            update_order = super().update(instance, validated_data)
            update_order.positions.all().delete()
            to_save = []
            for position in products:
                to_save.append(OrderPositions.objects.create(
                    order=update_order,
                    product=position["product"],
                    quantity=position["quantity"]
                ))
            return update_order


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collections
        fields = ["id", "header", "text", "created_date", "updated_date", "product"]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
