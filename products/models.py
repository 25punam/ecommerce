from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def total_price(self):
        return self.quantity * self.product.price
    

class Order(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)  
    quantity = models.PositiveIntegerField(default=1)    
    status = models.CharField(max_length=20, default='Pending')  

    def __str__(self):
        return f"Order {self.id} - {self.status}"
    






