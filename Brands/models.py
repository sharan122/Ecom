from django.db import models

class Brand(models.Model):
    brand_name=models.CharField()
    status=models.BooleanField(default=True)
