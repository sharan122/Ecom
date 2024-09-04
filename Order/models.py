from django.db import models
from Accounts.models import CustomUser
from Product.models import variant

# Create your models here.
class Shippment_address(models.Model):
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
class Order(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address_id=models.ForeignKey(Shippment_address,on_delete=models.CASCADE)
    total_price = models.IntegerField()
    status=models.CharField(max_length=40)
    created_at=models.DateTimeField(auto_now_add=True)
    payment_type=models.CharField()
    
class Order_item(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id=models.ForeignKey(variant,on_delete=models.CASCADE)
    qty = models.IntegerField()
    total_price = models.IntegerField()
    status=models.CharField(max_length=40,default='Pending')
    
      
    