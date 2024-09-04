from django.db import models
from Accounts.models import CustomUser


# Create your models here.
class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(null=False,blank=False)
    state=models.CharField()
    pincode=models.PositiveIntegerField()
    city=models.CharField()
    email=models.EmailField(blank=True,null=True,)
    phone_no=models.CharField(max_length=13)
    address=models.TextField()
    landmark=models.TextField(null=True,blank=True)
    status=models.BooleanField(default=True)
    default=models.BooleanField(default=False)
    