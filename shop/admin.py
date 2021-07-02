from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Orders, Product, OrderPositions, ProductComment, Collections


class CollectionInline(admin.TabularInline):
    model = Collections.product.through
    extra = 1


class IsUserAdmin(UserAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "is_staff")
    list_filter = ("is_staff", )
    readonly_fields = ["username", "first_name", "last_name", "email"]


class ProductAdmin(admin.ModelAdmin):
    list_filter = ("name", "created_date", "price", "updated_date")
    list_display = ("id", "name", "price", "created_date")


class OrderPositionsInline(admin.TabularInline):
    model = OrderPositions
    readonly_fields = ("order", "product", "quantity")
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderPositionsInline, )
    list_filter = ("order_status", "created_date", "updated_date", "total_quantity", "total_sum")
    list_display = ("id", "user", "order_status", "created_date", "total_quantity", "total_sum")
    readonly_fields = ("total_quantity", "user", "total_sum", )
    list_select_related = ("user", )


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "product", "rating", "created_date", "updated_date")
    readonly_fields = ("user", "comment", "product", "rating", "created_date", "updated_date")
    list_filter = ("product", "rating", "created_date", "updated_date")
    list_select_related = ("user", )


class CollectionsAdmin(admin.ModelAdmin):
    list_filter = ("created_date", "updated_date")
    list_display = ("header", "created_date")
    readonly_fields = ("created_date", "product")
    inlines = [CollectionInline]


admin.site.register(User, IsUserAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(Collections, CollectionsAdmin)
