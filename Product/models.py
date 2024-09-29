from django.db import models
from Brands.models import Brand
from Accounts.models import CustomUser
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    camera = models.CharField(max_length=100)
    display_type = models.CharField(max_length=100)
    display_size = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    battery = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    network_type = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='Product')
   
    def __str__(self):
        return self.name

class variant(models.Model): 
    image1 = models.ImageField(upload_to='products/', null=False,blank=False)
    image2 = models.ImageField(upload_to='products/', null=False,blank=False) 
    image3 = models.ImageField(upload_to='products/', null=False,blank=False)  
    image4 = models.ImageField(upload_to='products/', null=True, blank=True)  
    ram = models.IntegerField()
    rom = models.IntegerField()
    color = models.CharField(max_length=30)
    qty = models.IntegerField()
    price = models.IntegerField(null=True,blank=True)
    status = models.BooleanField(default=True)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Review(models.Model):
    product_id = models.ForeignKey(variant,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    