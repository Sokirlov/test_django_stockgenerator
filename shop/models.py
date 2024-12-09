import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from smart_selects.db_fields import ChainedForeignKey

from settings import settings
from .consumers import broadcast_price_update
from shop_settings.models import Currency


class BaseShopModel(models.Model):
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name="%(class)s_created_by")
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="%(class)s_updated_by")

    class Meta:
        abstract = True

class Goods(BaseShopModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-create']
        verbose_name = 'Goods'
        verbose_name_plural = 'Goods'

    def __str__(self):
        return self.name

class Sale(BaseShopModel):
    name = models.CharField(max_length=250)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods = models.ManyToManyField(Goods, related_name="sale", blank=True)

    def update_price(self):
        discount_goods = self.goods.filter(is_active=True)
        for goods_ in discount_goods:
            price = goods_.prices.filter(is_active=True)
            if price.count() > 0:
                currency = price.first().currency
            else:
                try:
                    currency = Currency.objects.first()
                except Currency.DoesNotExist:
                    raise Exception('create currency')

            random_amount = round(random.uniform(float(self.min_price), float(self.max_price)), 2)
            goods_.prices.create(base_price=random_amount, currency=currency)

    def __str__(self):
        return self.name

class Price(BaseShopModel):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='prices', null=True, blank=True, )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_in_currency(self):
        price_ = float(self.base_price) * self.currency.exchange_rate
        return round(price_, 2)

    class Meta:
        ordering = ['-create']


    def __str__(self):
        return f"{self.goods.name} - {self.base_price}"

@receiver(pre_save, sender=Price)
def ensure_single_active_price(sender, instance, **kwargs):
    if instance.is_active:
        Price.objects.filter(goods=instance.goods, is_active=True).exclude(pk=instance.pk).update(is_active=False)

@receiver(post_save, sender=Price)
def price_updated(sender, instance, **kwargs):
    broadcast_price_update(instance)

class Order(BaseShopModel):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'is_active': True})
    price = ChainedForeignKey(Price, chained_field="good", chained_model_field="good", show_all=False,
                              auto_choose=True, sort=True, limit_choices_to={'is_active': True})
    amount = models.IntegerField(default=1)
    order_sum = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    # @property
    def get_summ_order(self):
        fix = self.price.price_in_currency * self.amount + settings.FIXED_PRICE
        percent = (self.price.price_in_currency * self.amount) * (1.0 + settings.PERCENTE * 0.01)
        return round(fix + percent, 2)


    def save(self, *args, **kwargs):
        if not self.order_sum:
            self.order_sum = self.get_summ_order()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-create']


    def __str__(self):
        return f"{self.user} - {self.goods.name} - {self.order_sum}"