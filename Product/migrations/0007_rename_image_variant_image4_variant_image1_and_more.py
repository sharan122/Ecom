# Generated by Django 5.0.7 on 2024-08-17 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_alter_product_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='image',
            new_name='image4',
        ),
        migrations.AddField(
            model_name='variant',
            name='image1',
            field=models.ImageField(default='products/temp.png', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image2',
            field=models.ImageField(default='products/temp.png', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image3',
            field=models.ImageField(default='products/temp.png', upload_to='products/'),
        ),
    ]
