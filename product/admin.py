from django.contrib import admin

# Register your models here.
from .models import Products, ProductPriceRanges

admin.site.register(Products)
admin.site.register(ProductPriceRanges)