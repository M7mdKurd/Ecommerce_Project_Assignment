from django.contrib import admin

from products.models import Products, Category

admin.site.register(Category)
admin.site.register(Products)