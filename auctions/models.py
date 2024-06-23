from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import Permission
from django import forms
from django.utils.timezone import now
from datetime import datetime
import pytz

# CATEGORY = (
#     ('fashion', 'fashion'), 
#     ('toys', 'toys'),
#     ('electronics', 'electronics'), 
#     ('home', 'home'), 
#     ('sports', 'sports'),
#     ('pets', 'pets'), 
#     ('baby', 'baby'), 
#     ('grocery','grocery'), 
#     ('entertainment','entertainment'),
#     )

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class  Listing(models.Model):
    productnames = models.CharField(max_length=20)
    # productnames = ["hti"]
    descriptions = models.TextField(max_length=500)
    startingbids = models.DecimalField(max_digits=15, decimal_places=2)
    images = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True, default="")
    lister = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)
    timer = models.DateTimeField(default=now)
    # today = models.DateTimeField(default=now)
    today = now()
    minimum_charge = models.IntegerField(default=19)
    is_active = models.CharField(max_length=1, default='Y')
    # close_time = models.DateTimeField(null=True)
    # now_asia = datetime.now().astimezone(pytz.utc)

    print("hi",today)
    # price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        # print("hiiii",str(self.timer))
        return self.productnames

class Bidding(models.Model):
    bidder = models.CharField(max_length=50, blank=True, null=True)
    bidprice = models.IntegerField()
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

class Watchlist(models.Model):
    productnames = models.CharField(max_length=20)
    images = models.URLField(blank=True, null=True)
    finalbid = models.DecimalField(max_digits=15, decimal_places=2)
    lister = models.CharField(max_length=50, blank=True, null=True)
    watcher = models.CharField(max_length=50, blank=True, null=True)
    listingid = models.IntegerField()
    isActive = models.CharField(max_length=1, default='Y')

    def __str__(self):
        return f"{self.listingid}"

class  Closebid(models.Model):
    productnames = models.CharField(max_length=20)
    images = models.URLField(blank=True, null=True)
    lister = models.CharField(max_length=64, blank=True, null=True)
    bidder = models.CharField(max_length=64, blank=True, null=True)
    listingid = models.IntegerField()
    category = models.CharField(max_length=50, blank=True, null=True)
    finalbid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    closed_time = models.DateTimeField(default=now)
    paid_time = models.DateTimeField(null=True)
    is_active = models.CharField(max_length=1,default='Y')

    def __str__(self):
        return f"{self.id}"

class Comment(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(default=now, editable=False)
    comment = models.CharField(max_length=30)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"


class MyCoin(models.Model):
    id = models.IntegerField(primary_key=True)
    # productnames = ["hti"]
    username = models.TextField(max_length=500)
    coins_available = models.IntegerField(default=0)
    # images = models.URLField(blank=True, null=True)
    # category = models.CharField(max_length=50, blank=True, null=True, default="")
    # lister = models.CharField(max_length=50, blank=True, null=True)
    # created = models.DateTimeField(default=now, editable=False)
    # timer = models.DateTimeField(default=now)
    # # today = models.DateTimeField(default=now)
    today = now()
    # now_asia = datetime.now().astimezone(pytz.utc)

    print("hi",today)
    # price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        # print("hiiii",str(self.timer))
        return self.username

class Registraction_Fees(models.Model):
    current_charges = models.IntegerField(default=0)
    def __str__(self):
        return self.id

def increment_six_digit_id():
    last_record = Transactions.objects.all().order_by('transaction_id').values('transaction_id').last()
    # print("last" ,last_record)
    # last_record =767
    if last_record:
        last_id = last_record['transaction_id']
        new_id = last_id + 1
    else:
        # Set an initial value (e.g., 100000) if no records exist yet
        new_id = 100000
    return new_id
class Transactions(models.Model):
    # db_table = 'auctions_cointransactions'
    transaction_id = models.IntegerField(default=increment_six_digit_id, unique=True)
    username = models.TextField(max_length=500, null=False)
    coins = models.IntegerField(default=0)
    entry_at = models.DateTimeField(default=now)
    t_status = models.CharField(max_length=1, null=True)
    error = models.CharField(max_length=50, null=True)
    cause = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username

class Address(models.Model):
    # pass
    # user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    username = models.TextField(max_length=500, null=True)
    address_type = models.CharField(max_length=20, choices=(('billing', 'Billing'), ('shipping', 'Shipping')), default='billing')

    first_name = models.CharField( max_length=50,null=True)
    last_name = models.CharField( max_length=50,null=True)
    street_address = models.CharField( max_length=200,null=True)
    city = models.CharField( max_length=100, null=True)
    state = models.CharField( max_length=100,null=True)
    pin_code = models.CharField( max_length=10,null=True)
    mobile_no = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$', 'Only numbers are allowed')],null=True)
    alternate_no =  models.CharField( max_length=10, validators=[RegexValidator(r'^[0-9]+$', 'Only numbers are allowed')],null=True)
    def __str__(self):
        return f"{self.user.username}'s {self.get_address_type_display()}"

class  Bid_History(models.Model):
    # productnames = models.CharField(max_length=20)
    listingid = models.IntegerField()
    username = models.TextField(max_length=500)
    bid_price =models.DecimalField(max_digits=15, decimal_places=2)
    update_time = models.DateTimeField(default=now)


    def __str__(self):
        # print("hiiii",str(self.timer))
        return self.listingid

class Coupon(models.Model):

    # id = models.IntegerField(primary_key=)
    coupon_code = models.TextField(max_length=50)
    discount = models.IntegerField()
    minimum_order_val = models.IntegerField()
    isActive = models.CharField( max_length=1)
    creation_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.id