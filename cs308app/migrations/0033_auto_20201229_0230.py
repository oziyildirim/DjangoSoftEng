# Generated by Django 3.0.5 on 2020-12-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0032_order_alldelivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='base_price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]