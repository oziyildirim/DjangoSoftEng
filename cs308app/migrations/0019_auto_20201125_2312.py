# Generated by Django 3.0.5 on 2020-11-25 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0018_auto_20201124_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='validation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='recommended',
            field=models.BooleanField(default=False),
        ),
    ]
