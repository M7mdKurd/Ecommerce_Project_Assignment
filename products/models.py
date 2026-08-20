from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    @property
    def count_products(self):
        return self.products_set.count()



class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(default='No_Image_Available.jpg' ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_choices = (
    (True, 'Active'),
    (False, 'inactive')
    )
    status = models.BooleanField(choices=status_choices , default=True)


    def decrease_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.save()
