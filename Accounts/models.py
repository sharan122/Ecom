
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    is_active= models.BooleanField(default=False)
    signup_method = models.CharField(default='google')
    

