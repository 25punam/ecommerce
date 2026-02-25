from django.contrib import admin
from .models import ProductModel,CartModel, Order
# Register your models here.

admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(Order)

#   
