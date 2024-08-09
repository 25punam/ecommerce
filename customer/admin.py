from django.contrib import admin
from .models import CustomerModel, ProductModel ,CartModel

# Register your models here.

admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(CartModel)
