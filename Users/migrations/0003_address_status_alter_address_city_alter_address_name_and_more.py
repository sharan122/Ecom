# Generated by Django 5.0.7 on 2024-08-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_address_phone_no_alter_address_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(),
        ),
    ]
