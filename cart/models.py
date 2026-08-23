import decimal

from django.contrib.auth.models import User
from django.db import models

from products.models import Products


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


    @property
    def item_total(self):
        return decimal.Decimal(self.quantity) * self.product.price
