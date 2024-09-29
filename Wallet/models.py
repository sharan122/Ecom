from django.db import models
from Accounts.models import CustomUser

# Create your models here.


class Wallet(models.Model):
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0.00,max_digits=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    message = models.CharField( max_length=50)
    Amount = models.IntegerField(null=True,blank=True) 
    transaction_type = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    