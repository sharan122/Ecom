from django.db import models
from Product.models import variant
from Brands.models import Brand

# Create your models here.
class Product_Offers(models.Model):
    product_id = models.ForeignKey(variant,on_delete=models.CASCADE)
    offer_price = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    
class Brand_Offers(models.Model):
    brand_id = models.ForeignKey(Brand,on_delete=models.CASCADE)
    offer_price = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    