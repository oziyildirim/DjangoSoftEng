# Generated by Django 3.1.3 on 2020-11-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0016_auto_20201123_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(default=111111, max_length=6),
            preserve_default=False,
        ),
    ]
