from django.db import models
from Accounts.models import CustomUser
from Product.models import variant

# Create your models here.


class Cart(models.Model):
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Cart_item(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(variant,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price= models.IntegerField(default=0)
    
    @property
    def total_price(self):
        return self.qty*self.product.price