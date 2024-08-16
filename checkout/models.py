from django.db import models
from customer.models import User, CustomerModel
from products.models import ProductModel ,Order

# Create your models here.
class CustomerPaymentDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  
    status = models.CharField(max_length=20, default='Pending')  # Added status for tracking payment state

    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id} - Status: {self.status}"


class ProductReview(models.Model):
    user = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.name or self.user.username}"
    