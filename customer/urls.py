from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create_product),
    path('delete/', views.delete_product),
]
