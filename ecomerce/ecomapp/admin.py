from django.contrib import admin
from ecomapp.models import Products
class ProductsAdmin(admin.ModelAdmin):
    list_display=['name','price','cat']
    list_filter=['price','cat']
admin.site.register(Products,ProductsAdmin)
