from django.db import models
from django.contrib.auth.models import User

class CustomerModel(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name or self.user.username








