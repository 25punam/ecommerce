from django.db import models
from customer.models import User
from products.models import Order

# Create your models here.
class CustomerPaymentDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  
    status = models.CharField(max_length=20, default='Pending')
    shipping_address = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id} - Status: {self.status}"


