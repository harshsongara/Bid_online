# Generated by Django 3.1 on 2024-06-23 06:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.TextField(max_length=50)),
                ('discount', models.IntegerField()),
                ('minimum_order_val', models.IntegerField()),
                ('isActive', models.CharField(max_length=1)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]