from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.CharField(
        'ТГ-ник пользователя',
        max_length=200,
    )
    phone = models.CharField(
        'Номер телефона пользователя',
        max_length=200,
        blank=True,
        null=True
    )
    mail = models.CharField(
        'Почта пользователя',
        max_length=200,
        blank=True,
        null=True
    )
    adress = models.CharField(
        'Адрес пользователя',
        max_length=200,
        blank=True,
        null=True
    )
    amount = models.PositiveIntegerField(
        'Цена заказа',
        help_text='Цена заказа',
        default=0
    )
    payment = models.CharField(
        'id платежа',
        max_length=200,
        blank=True,
        null=True
    )
    close = models.BooleanField(
        'Заказ оплачен',
        help_text='Заказ оплачен',
        default=False,
    )
    close_data = models.DateField(
        "Дата покупки",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.user}, {"Закрыт" if self.close else "Не закрыт"}'


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_order',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        'Количество товара в заказе',
        help_text='Количество товара в заказе',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='product_order',
        verbose_name='Заказ',
    )

    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказы товаров'

    def __str__(self):
        return f"В {self.order} {self.quantity} {self.product}"
