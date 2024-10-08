# Generated by Django 5.0.7 on 2024-09-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=250)),
                ('coupon_code', models.CharField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('percentage', models.IntegerField()),
                ('max_amount', models.IntegerField()),
                ('expiry', models.DateField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
