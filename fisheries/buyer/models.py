from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('FISHER', 'Fisher'),
        ('BUYER', 'Buyer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def is_fisher(self):
        return self.user_type == 'FISHER'
    
    def is_buyer(self):
        return self.user_type == 'BUYER'
