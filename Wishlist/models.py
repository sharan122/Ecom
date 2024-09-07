from django.db import models
from Product.models import variant
from Accounts.models import CustomUser

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(variant,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)