from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StatusChoices(models.TextChoices):
    NEW = "open", "Новый"
    PROCESS = "process", "В процессе"
    DONE = "done", "Выполнен"


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    pass


class Orders(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    order_status = models.CharField(
        "Статус заказа",
        max_length=225,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW
    )
    created_date = models.DateField("Дата создания", auto_now_add=True)
    updated_date = models.DateField("Дата обновления", auto_now=True)
    total_quantity = models.IntegerField("Общ. количество товаров в заказе")
    total_sum = models.DecimalField(
        "Общая сумма заказа",
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Product(models.Model):
    name = models.CharField("Название", max_length=225)
    description = models.CharField("Описание", max_length=400)
    price = models.DecimalField(
        "Цена",
        max_digits=9,
        decimal_places=2
    )
    created_date = models.DateField("Дата создания", auto_now_add=True)
    updated_date = models.DateField("Дата обновления", auto_now=True)
    photo = models.URLField(
        "Фото",
        null=True,
        blank=True,
        default="https://ricesplash.learningu.org/media/images/not-available.jpg"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class OrderPositions(models.Model):
    order = models.ForeignKey(
        Orders,
        verbose_name="Заказ",
        on_delete=models.CASCADE,
        related_name="positions"
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="positions"
    )
    quantity = models.IntegerField("Количество")

    def __str__(self):
        return f"{self.order}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"


class ProductComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    comment = models.CharField("Отзыв", max_length=250)
    rating = models.IntegerField(
        "Оценка",
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
    created_date = models.DateField("Дата создания", auto_now_add=True)
    updated_date = models.DateField("Дата обновления", auto_now=True)

    def __str__(self):
        return f"{self.comment}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Collections(models.Model):
    header = models.CharField("Заголовок", max_length=100)
    text = models.CharField("Описание", max_length=400)
    created_date = models.DateField("Дата создания", auto_now_add=True)
    updated_date = models.DateField("Дата обновления", auto_now=True)
    product = models.ManyToManyField(
        Product,
        verbose_name="Продукт",
        related_name='collections'
    )

    def __str__(self):
        return f"{self.header}"

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
