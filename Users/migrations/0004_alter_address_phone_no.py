# Generated by Django 5.0.7 on 2024-08-27 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_address_status_alter_address_city_alter_address_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.CharField(max_length=13),
        ),
    ]
