from django.urls import path,include
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('paypal/', include('paypal.standard.ipn.urls')), 
    path('process_paypal_payment/<int:order_id>/<str:amount>/<int:user_id>/', views.process_paypal_payment, name='process_paypal_payment'),
]
