# Generated by Django 3.1.3 on 2020-12-02 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0019_auto_20201125_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cs308app.user'),
        ),
    ]
