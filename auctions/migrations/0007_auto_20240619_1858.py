# Generated by Django 3.1 on 2024-06-19 13:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20240619_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile_no',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9]+$', 'Only numbers are allowed')]),
        ),
    ]
