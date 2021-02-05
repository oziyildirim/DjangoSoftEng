# Generated by Django 3.0.5 on 2021-01-03 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs308app', '0034_campaigninfo_campaignitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCancel',
            fields=[
                ('ordercancel_id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cs308app.Order')),
            ],
        ),
    ]
