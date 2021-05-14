from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StatusChoices(models.TextChoices):
    NEW = "open", "Новый"
    PROCESS = "process", "В процессе"
    DONE = "done", "Выполнен"


class User(AbstractUser):
    pass


class Orders(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    order_status = models.CharField(
        max_length=225,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW
    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    total_quantity = models.IntegerField()
    total_sum = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.user}"


class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=400)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    photo = models.URLField(
        null=True,
        blank=True,
        default="https://ricesplash.learningu.org/media/images/not-available.jpg"
    )

    def __str__(self):
        return f"{self.name}"


class OrderPositions(models.Model):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        related_name="positions"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="positions"
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order}"


class ProductComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    comment = models.CharField(max_length=250)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(
                limit_value=5,
                message=f"you can't rate more than 5"),
            MinValueValidator(
                limit_value=1,
                message=f"you can't rate less than 1"
            )
        ]

    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"


class Collections(models.Model):
    header = models.CharField(max_length=100)
    text = models.CharField(max_length=400)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    product = models.ManyToManyField(
        Product,
        related_name='collections'
    )

    def __str__(self):
        return f"{self.header}"
