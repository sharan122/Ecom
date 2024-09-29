from django.db import models
from Accounts.models import CustomUser

# Create your models here.

class Coupons(models.Model):
    description = models.TextField(max_length=250)
    coupon_code = models.CharField(blank = False,null=False)
    created_at = models.DateField(auto_now_add=True)
    percentage = models.IntegerField()
    max_amount = models.IntegerField()
    min_amount = models.IntegerField(default=0)
    expiry = models.DateField()
    status = models.BooleanField(default=True)

class Coupon_users(models.Model):
    user_id  = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    coupon_code  = models.ForeignKey(Coupons,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    