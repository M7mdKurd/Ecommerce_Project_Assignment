import decimal

from django.contrib.auth.models import User
from django.db import models
from products.models import Products


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.TextField()
    order_status_choices = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    order_status = models.CharField(max_length=10, choices=order_status_choices, default='pending')



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()



    @property
    def item_total(self):
        return self.quantity * self.product.price



