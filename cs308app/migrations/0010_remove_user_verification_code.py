# Generated by Django 3.1.3 on 2020-11-19 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0009_auto_20201118_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
    ]
