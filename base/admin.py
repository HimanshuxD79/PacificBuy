from django.contrib import admin
from .models import (
    Customers,
    Product,
    Cart,
    OrderPlaced,
)
# Register your models here.
@admin.register(Customers)
class CustomerAdminModel(admin.ModelAdmin):
    list_display=['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display=['id', 'title', 'selling_price', 'discounted_price',  'description', 'brand', 'category', 'product_image']    

@admin.register(Cart)
class CartAdminModel(admin.ModelAdmin):
    list_display=['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedAdminModel(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'product', 'quantity', 'order_date', 'status']