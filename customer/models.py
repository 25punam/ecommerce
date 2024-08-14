from django.db import models
from django.contrib.auth.models import User


class CustomerModel(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name or self.user.username


class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price


class OrderModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20, default="Pending"
    )  # Added status field for order tracking

    def __str__(self):
        return f"Order for {self.cart.product.name} on {self.order_date}"


class CustomerPaymentDetails(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, default="Pending"
    )  # Added status for tracking payment state

    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id} - Status: {self.status}"


class ProductReview(models.Model):
    user = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_count = models.PositiveIntegerField(
        default=0
    )  # Added for tracking helpful votes

    def __str__(self):
        return (
            f"Review for {self.product.name} by {self.user.name or self.user.username}"
        )
