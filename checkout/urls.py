from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]
