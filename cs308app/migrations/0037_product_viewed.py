# Generated by Django 3.1.4 on 2021-01-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0036_order_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='viewed',
            field=models.IntegerField(default=0),
        ),
    ]
