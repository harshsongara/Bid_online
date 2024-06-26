# Generated by Django 3.1 on 2024-06-16 12:37

import auctions.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidder', models.CharField(blank=True, max_length=50, null=True)),
                ('bidprice', models.IntegerField()),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Closebid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productnames', models.CharField(max_length=20)),
                ('images', models.URLField(blank=True, null=True)),
                ('lister', models.CharField(blank=True, max_length=64, null=True)),
                ('bidder', models.CharField(blank=True, max_length=64, null=True)),
                ('listingid', models.IntegerField()),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('finalbid', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('comment', models.CharField(max_length=30)),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productnames', models.CharField(max_length=20)),
                ('descriptions', models.TextField(max_length=500)),
                ('startingbids', models.DecimalField(decimal_places=2, max_digits=15)),
                ('images', models.URLField(blank=True, null=True)),
                ('category', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('lister', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('timer', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='MyCoin',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.TextField(max_length=500)),
                ('coins_available', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Registraction_Fees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_charges', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.IntegerField(default=auctions.models.increment_six_digit_id, unique=True)),
                ('username', models.TextField(max_length=500)),
                ('coins', models.IntegerField(default=0)),
                ('entry_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('t_status', models.CharField(max_length=1, null=True)),
                ('error', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productnames', models.CharField(max_length=20)),
                ('images', models.URLField(blank=True, null=True)),
                ('finalbid', models.DecimalField(decimal_places=2, max_digits=15)),
                ('lister', models.CharField(blank=True, max_length=50, null=True)),
                ('watcher', models.CharField(blank=True, max_length=50, null=True)),
                ('listingid', models.IntegerField()),
                ('isActive', models.CharField(default='N', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], default='billing', max_length=20)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('street_address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(max_length=2, null=True)),
                ('pin_code', models.CharField(max_length=10, null=True)),
                ('mobile_no', models.CharField(max_length=10, null=True)),
                ('alternate_no', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
