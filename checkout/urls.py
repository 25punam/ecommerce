from django.urls import path,include
from . import views

urlpatterns = [
    path('checkout/', views.checkout,name='checkout'),
    path('order_success/', views.order_success,name='order_success'),
    path('paypal/',include('paypal.standard.ipn.urls')),
]    