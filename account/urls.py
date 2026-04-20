from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('check_username/', views.check_username_availability, name='check_username'),
    path('check_email/', views.check_email_availability, name='check_email'),
]