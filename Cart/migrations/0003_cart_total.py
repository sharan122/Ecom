# Generated by Django 5.0.7 on 2024-09-12 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0002_cart_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
