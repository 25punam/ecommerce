from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart_detail/<int:product_id>', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order_list/', views.order_list, name='order_list'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]    