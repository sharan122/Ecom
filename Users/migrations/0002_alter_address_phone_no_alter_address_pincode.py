# Generated by Django 5.0.7 on 2024-08-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.PositiveIntegerField(),
        ),
    ]
