# Generated by Django 5.0.7 on 2024-09-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0006_order_item_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='message',
            field=models.CharField(),
        ),
    ]
