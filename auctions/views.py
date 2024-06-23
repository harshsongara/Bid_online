from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max
from django.contrib.sessions.models import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import now
from datetime import datetime
from django.utils import timezone
# now = timezone.now()
# import pytz
# tz = pytz.timezone('Asia/Kolkata')

from .models import Bid_History, User, Listing, Bidding, Watchlist, Closebid, Comment, Category, MyCoin, Coupon, Address,Transactions

from .forms import ListingForm, BiddingForm, CommentForm, AddCoinForm, BillingAddressForm, ShippingAddressForm, SelectAddressForm
# from .task import my_background_task

def index(request):                                                             
    listing = Listing.objects.filter(is_active='Y')
    # now = datetime.now()
    # print(listing[9].timer)
    # print(listing[9].today)
    # print(listing[1].timer > listing[1].today)
    # print(listing[9].startingbids)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount=len(watch)
        # print(watchcount)
    except:
        watchcount=None
    return render(request, "auctions/index.html", {
        'object': listing,
        'watchcount': watchcount
    })

def add_transaction(**kwargs):
    # Create a new transaction instance
    print(kwargs['cause'])
    try:
        new_transaction = Transactions(
            username=kwargs['username'],
            coins=kwargs['coins'],  # Set the number of coins
            t_status=kwargs['t_status'],  # Set the status
            error = kwargs['error'],
            cause = kwargs['cause']
        )
        new_transaction.save()
    except:
        return 1
    return 0

@login_required
def createlisting(request):
    creator = Listing.objects.all()
    form = ListingForm(request.POST or None)
    auth_user = User.objects.filter(username=request.user).values('is_staff','is_superuser')[0]
    if not (auth_user["is_staff"] or auth_user["is_superuser"]):
        return HttpResponseRedirect(reverse('index'))
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    if request.method == "POST":
        print(form.is_valid())
        if form.is_valid():
            # print("submting")
        # if 1==1:
            now = datetime.now()                                                #save date created with current timezone
            fs = form.save(commit=False)
            fs.lister = request.user                                            #save info not listed at forms.py
            fs.created = now
            fs.save()
            # my_background_task('harshit','songara')
            messages.success(request, f'Listing added successfully "{fs.productnames}." ')
            return render(request, "auctions/create.html", {
                'form': form,
                'creator': creator,
                'watchcount': watchcount
            })
        else:
            print(form.errors)
            messages.error(request, f'{form.errors}')
            return render(request, "auctions/create.html", {
                'form': form,
                'creator': creator,
                'watchcount': watchcount
            })
    else:
        return render(request, "auctions/create.html", {
            'form': form,
            'creator': creator,
            'watchcount': watchcount
        })

def listingpage(request,id):
    listing = Listing.objects.get(id=id)
    # now = datetime.now()
    # print(type(listing.today))
    # print(listing.timer,now())
    # if listing.timer < now():
    #     print("Bind ended")
    comment = Comment.objects.filter(listingid=id)
    # print("h",request.POST.get("bidprice"))
    try:
        cform = CommentForm(request.POST or None)
        bidform = BiddingForm(request.POST or None)
        print(bidform)
    except:
        return redirect('index')
    if request.user.username:
        try:
            if Watchlist.objects.get(watcher=request.user.username, listingid=id):
                added=True
        except:
            added = False
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount=None
        try:
            ccount = Comment.objects.filter(listingid=id)
            ccount = len(ccount)
        except:
            ccount = len(ccount)
        try:
            users = User.objects.raw("select id, username from auctions_user where is_superuser=1 or is_staff=1")
            closerUsers = [user.username for user in users]

            if request.user.username in closerUsers:
                lister = True
            else:
                lister = False
        except:
            return redirect('index')

        # for user in users:
        #     closerUsers.append(user.username)
        # print(closerUsers)
    else:
        ccount = Comment.objects.filter(listingid=id)
        ccount = len(ccount)
        added = False
        lister = False
        watchcount = None
    try:
        bid = Bid_History.objects.filter(listingid=id)
        bidcount = len(bid)
        listing = Listing.objects.get(id=id)
    except:
        bicount = None
    # print("kkkkkkkk",now)
    return render(request, "auctions/listing.html", {
        'object': listing,
        'added': added,
        'bidform': bidform,
        "watchcount": watchcount,
        "error":request.COOKIES.get('error'),
        "success":request.COOKIES.get('success'),
        "bidcount": bidcount,
        "lister": lister,
        'cform': cform,
        "comment": comment,
        "ccount": ccount,
        "now": now
    })

@login_required
def addwatch(request, id):
    if request.user.username:
        listing = Listing.objects.get(id=id)
        watchers = Watchlist(watcher = request.user.username, listingid = id)
        watchers.lister = listing.lister
        watchers.finalbid = listing.startingbids
        watchers.productnames = listing.productnames
        watchers.images = listing.images
        watchers.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
def removewatch(request,id):
    if request.user.username:
        try:
            Watchlist.objects.filter(listingid=id).delete()
            return redirect('listingpage', id=id)
        except:
            return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
def watchlist(request):

    try:
        # watchlist = Watchlist.objects.filter(watcher=request.user.username, isActive='Y')
        # closebid = Closebid.objects.filter(bidder=request.user.username)
        watchlist = Watchlist.objects.raw(f"select * from (SELECT *,row_number() over(PARTITION by listingid order by finalbid desc) as rn FROM auctions_watchlist where watcher = '{request.user.username}' and isActive='Y') where rn=1")
        watchcount = len(watchlist)                                                 #count how many rows in table Watchlist using len()
        print(watchcount)
        watchlistids = [listid.listingid for listid in watchlist]

    except:
        watchcount = None
        watchlistids = [0]

    # Added by Harsh
    try:
    # if 1==1:
        HighestBidders = Watchlist.objects.filter(listingid__in=watchlistids, isActive='Y') \
            .values('listingid') \
            .annotate(highest_bid=Max('finalbid'))

        watcher_high_bids = []
        for higher in HighestBidders:
            listing_id = higher['listingid']
            highest_bid = higher['highest_bid']
            if highest_bid is not None:
                # Check if the watcher's bid matches the highest bid
                watcher_bid = Watchlist.objects.filter(listingid=listing_id, watcher=request.user.username)
                for watch in watcher_bid:
                    if watch and watch.finalbid == highest_bid:
                        watcher_high_bids.append(listing_id)

    except:
        watcher_high_bids = [0]
    print(watcher_high_bids)
    try:
        closebid = Closebid.objects.filter(bidder = request.user.username, is_active = 'Y')
        bidwincount = len(closebid)
    except:
        binwincoun = None
    try:
        if Watchlist.objects.get(listingid=listingid):
            closed = True
        else:
            closed = False
    except:
        closed = False

    return render(request, "auctions/watchlist.html", {
        'object': watchlist,
        "watchcount": watchcount,
        "closedbid": closebid,
        "closed" : closed,
        "bidwincount": bidwincount,
        "highBids": watcher_high_bids
    })

@login_required
def bid(request, listingid):
    listings = Listing.objects.get(id=listingid)
    existing_coin = MyCoin.objects.filter(username=request.user).values('coins_available')[0]["coins_available"]
    # minimum_balance_required =Registraction_Fees.objects.values("current_charges")[0]["current_charges"]
    # print(minimum_balance_required)
    # print(listings.id)
    minimum_balance_required = listings.minimum_charge
    current = listings.startingbids
    bidform = BiddingForm(request.POST or None)
    if request.user.username:
        bid = float(request.POST.get("bidprice"))

        if bid > current:
            is_userAlreadyRegisterd = Bid_History.objects.filter(listingid= listingid,username = request.user.username).count()
            print("is_userAlreadyRegisterd",is_userAlreadyRegisterd)
            if existing_coin < minimum_balance_required and is_userAlreadyRegisterd == 0 :
                response = redirect('listingpage', id=listingid)
                response.set_cookie('error',f'Minimum {minimum_balance_required} coins are required to register!', max_age=1)
                return response
            listing = Listing.objects.get(id=listingid)
            listing.startingbids = bid
            listing.save()
            try:
                # if Bidding.objects.filter(id=listingid):
                #     bidrow = Bidding.objects.filter(id=listingid)
                #     bidrow.delete()
                fs = bidform.save(commit=False)
                fs.bidder = request.user.username
                fs.listingid = listingid
                fs.save()                                                      
            except:
                fs = bidform.save(commit=False)
                fs.bidder = request.user
                fs.listingid = listingid
                fs.save()

            response = redirect('listingpage', id=listingid)
            response.set_cookie('success','Successful Bid! Your bid is currently the highest bid.', max_age=1)
            addwatch(request, listingid)
            bid_history_entry = Bid_History(
                listingid=listingid,  # Set the listing ID
                username=request.user.username,  # Set the username
                bid_price=bid  # Set the bid price
            )
            bid_history_entry.save()
            coin_deducted = Bid_History.objects.filter(username = request.user.username, listingid=listingid).count()
            print(coin_deducted)
            if coin_deducted == 1:
                transact = add_transaction(username=request.user.username,coins=-minimum_balance_required,t_status= 'Y',error=None,cause=f"Refundable registration charges for {listings}")
                if transact == 0:
                    existing_coin = MyCoin.objects.get(username=request.user)
                    existing_coin.coins_available-=minimum_balance_required
                    # existing_coin.coins_available = coins+existing_coin.values('coins_available')[0]["coins_available"]
                    existing_coin.save()

            return response
        else:
            response = redirect('listingpage', id=listingid)
            response.set_cookie('error','Your bid must be higher than the current price!', max_age=1)
            return response
    else:
        return redirect('index')
        
@login_required
def closebid(request, listingid):
    if request.user.username:
        try:
            listing = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        closebid = Closebid()
        name = listing.productnames
        closebid.lister = listing.lister
        closebid.listingid = listingid
        closebid.productnames = listing.productnames
        closebid.images = listing.images
        closebid.category = listing.category
        try:
        # if 1==1:
            bid = Bid_History.objects.raw(f"""select id, username, bid_price from (
            select *,row_number() over(order by bid_price desc) as rn  from auctions_bid_history where listingid = {listingid} 
            ) where rn=1""")[0]
            # print(bid)
            closebid.bidder = bid.username
            closebid.finalbid = bid.bid_price
            closebid.save()
            # bid.delete()
        except:
            closebid.bidder = listing.lister
            closebid.finalbid = listing.startingbids
            closebid.save()
            unique_usernames = Bid_History.objects.filter(listingid=listingid).values('username').distinct()
            print(unique_usernames)

        # try:
        if 1==1:
            unique_usernames = Bid_History.objects.filter(listingid=listingid).values('username').distinct()
            usernames = list(all['username'] for all in unique_usernames)
            if bid.username in usernames:
                usernames.remove(bid.username)

            print('not kk',usernames)
            # add_transaction(username=request.user.username,coins=listing.minimum_charge,t_status='Y',error=None,cause=f'Refundend against {listing.productnames}.')
            coins = MyCoin.objects.filter(username__in = usernames)
            for coin in coins:
                print(coin)
                add_transaction(username=coin.username,coins=listing.minimum_charge,t_status='Y',error=None,cause=f'Refundend against {listing.productnames}.')
                coin.coins_available+=listing.minimum_charge
                coin.save()

        # except:
        #     print('kk')

        try:
            if Watchlist.objects.filter(listingid=listingid):
                watch = Watchlist.objects.filter(listingid=listingid)
                watch.delete()
            else:
                pass
        except:
            pass
        try:
            comment = Comment.objects.filter(listingid=listingid)
            comment.delete()
        except:
            pass
        # try:
        #     bid = Bid.objects.filter(listingid=listingid)
        #     bid.delete()
        # except:
        #     pass
        try:
            closebidlist = Closebid.objects.get(listingid=listingid)
        except:
            closebid.lister = listing.lister
            closebid.bidder = listing.lister
            closebid.listingid = listingid
            closebid.finalbid = listing.startingbids
            closebid.productnames = listing.productnames
            closebid.images = listing.images
            closebid.category = listing.category
            closebid.save()
            closebidlist = Closebid.objects.get(listingid=listingid)
        # listing.delete()
        listing.is_active = 'N'
        listing.save()
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount = None
        return render(request,"auctions/winner.html",{
            "closebidlist": closebidlist,
            "name": name,
            "watchcount":watchcount
        })   
    else:
        return redirect('index')

@login_required
def closed(request, listingid):
    closed = Closebid.objects.get(listingid=listingid)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    print(str(closed))
    request.session['selected_product_id'] = str(closed)
    # request.session['listingid']= str(listingid)

    return render(request, "auctions/closed.html", {
        "object": closed,
        "watchcount": watchcount
    })

@login_required
def comment(request, listingid):
    if request.method == "POST":
        comment = Comment.objects.all()
        cform = CommentForm(request.POST or None)
        if cform.is_valid():
            now = datetime.now()                                               
            fs = cform.save(commit=False)   
            fs.listingid = listingid
            fs.user = request.user.username                               
            fs.time = now
            fs.save()
        return redirect('listingpage', id=listingid)
    else:
        return redirect('index') 

def category(request):
    category = Category.objects.all()
    closedbid = Closebid.objects.all()
    try:
        if Watchlist.objects.get(listingid=listingid):
            closed = True
        else:
            closed = False
    except:
        closed = False
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, "auctions/categories.html", {
        "object": category,
        "watchcount": watchcount,
        "closed": closed,
        "closedbid": closedbid
    })

def categorylistings(request, cats):
    category_posts = Listing.objects.filter(category=cats)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, 'auctions/categorylistings.html', {
        'cats': cats,
        'category_posts': category_posts,
        'watchcount': watchcount
    })

def allclosed(request):
    closedlist = Closebid.objects.all()
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, 'auctions/allclosed.html', {
        'closedlist': closedlist,
        'watchcount': watchcount
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def coin(request):
    # print(request.user)
    # print(MyCoin.objects.values())

    coins = MyCoin.objects.filter(username = request.user).values('coins_available')[0]
    print(coins)
    try:
    # if 1==1:
        form = AddCoinForm(request.POST or None)
    except:
        # print('ere')
        return redirect('index')
    print(form)
    return render(request,"auctions/coins.html",{

        'form': form,
        'coins': coins,
        "error":request.COOKIES.get('error'),
        "success":request.COOKIES.get('success')

    })


@login_required
def addCoin(request):
    # current = Listing.objects.get(id=listingid)
    # minimum_balance_required =Registraction_Fees.objects.values("current_charges")[0]["current_charges"]
    # print(type(minimum_balance_required))
    # print(coins["coins_available"])
    # current = current.startingbids
    # coins = MyCoin.objects.filter(username = request.user).values('coins_available')[0]
    try:
        form = AddCoinForm(request.POST or None)
    except:

        return redirect('index')

    if request.user.username:
        coins = float(request.POST.get("coins"))
        print(type(coins))
    # coins = MyCoin.objects.filter(username=request.user).values('coins_available')[0]
    response = redirect('coin')
    if coins <= 0:
        response.set_cookie('error',f'Something went wrong please try again.', max_age=1)
        coin_added = 'N'
    elif coins <=9:
        response.set_cookie('error',f'mininum 10 coins can be added', max_age=1)
        coin_added = 'N'
    else:
        response.set_cookie('success','Coins added successfully .', max_age=1)
        coin_added = 'Y'

    fs = form.save(commit=False)
    fs.username = request.user.username
    fs.coins = coins
    print(coin_added)
    fs.t_status = coin_added
    fs.cause = "Coins are added manually."
    fs.save()
    try:
        if coin_added == 'Y':
            existing_coin = MyCoin.objects.get(username=request.user)
            ""
            existing_coin.coins_available+=coins
            # existing_coin.coins_available = coins+existing_coin.values('coins_available')[0]["coins_available"]
            existing_coin.save()
    except:
        fs = form.save(commit=False)
        fs.username = request.user.username
        fs.coins = -coins
        # print(coin_added)
        fs.t_status = 'N'
        fs.error = 'ERROR: Coins not added, Reverting'
        fs.save()
        response.delete_cookie('success')
        response.set_cookie('error',f'Something is not correct', max_age=1)

    return response

def select_address_view(request):
    existing_addresses = Address.objects.raw(f"""
    select * from 
    (select *,row_number() over(PARTITION by first_name,last_name, street_address,city, state, pin_code order by first_name,last_name, street_address,city, state, pin_code) as rn
     from auctions_address where username='{request.user.usename}')
     where rn=1
    """)

    if request.method == 'POST':
        form = SelectAddressForm(request.POST, user=request.user)
        if form.is_valid():
            selected_address = form.cleaned_data['address']
            request.session['selected_address_id'] = selected_address.id
            return redirect('payment_page')
    else:
        form = SelectAddressForm(username=request.user)

    return render(request, 'select_address.html', {'form': form,
                                                   'existing_addresses':existing_addresses
                                                   })

@login_required()
def selectAddress(request):
    existing_addresses = Address.objects.raw(f"""
    select * from 
    (select *,row_number() over(PARTITION by first_name,last_name, street_address,city, state, pin_code order by first_name,last_name, street_address,city, state, pin_code) as rn
     from auctions_address where username='{request.user.username}')
     where rn=1
    """)
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        # request.session['selected_address_id']  = selected_address_id
        # print(selected_address_id)
        print("address selected enterint to pay")
        return payment(request,selected_address_id)
        # return render(request,"auctions/select_address.html",{
        #     'existing_addresses':existing_addresses})

    return render(request,"auctions/select_address.html",{
        'existing_addresses':existing_addresses
        # 'coins': coins,
        # "error":request.COOKIES.get('error'),
        # "success":request.COOKIES.get('success')

    })

@login_required
def address(request):
    # print(request.session['id'])
    # existing_addresses = Address.objects.raw("""
    # select * from
    # (select *,row_number() over(PARTITION by first_name,last_name, street_address,city, state, pin_code order by first_name,last_name, street_address,city, state, pin_code) as rn
    #  from auctions_address)
    #  where rn=1
    # """)
    try:
        Bform = BillingAddressForm(request.POST or None, prefix='b')
        Sform = ShippingAddressForm(request.POST or None, prefix='s')

    except:
        return redirect('index')
    return render(request,"auctions/address.html",{
        'Bform': Bform,
        'Sform': Sform,
        # 'existing_addresses':existing_addresses
        # 'coins': coins,
        # "error":request.COOKIES.get('error'),
        # "success":request.COOKIES.get('success')

    })

def addAddress(request):
    try:
        # Bform = BillingAddressForm(request.POST or None, prefix='b')
        Sform = ShippingAddressForm(request.POST or None, prefix='s')
    except:
        return redirect('index')

    if Sform.is_valid():
        sf = Sform.save(commit=False)
        sf.address_type = 'shipping'
        sf.username = request.user.username
        sf.save()

        messages.success(request, 'Address added successfully.')
        return render(request,"auctions/address.html",{
            'Sform': Sform})
        # return redirect()
    else:
        messages.error(request, 'Something went wrong while adding address.')
        return render(request,"auctions/address.html",{
            'Sform': Sform})

def payment(request,address_id):
    id = request.session['selected_product_id']
    listingid = Closebid.objects.filter(id=id).values('listingid').first()['listingid']
    address = Address.objects.filter(id=address_id).first()
    print(listingid)
    # listingid = request.session['listingid']
    print(id)
    listings = Listing.objects.filter(id=listingid)
    print("inside payment")
    print(listings)

    print(address_id)
    try:
        closed = Closebid.objects.filter(id=id, bidder=request.user.username, is_active='Y').first()
    except:
        return redirect('index')

    try:
        coins = MyCoin.objects.filter(username = request.user.username).first()
        print(coins.coins_available)
        # print(coins['coins_available'])
    except:
        return redirect('index')

    try:
        coupons = Coupon.objects.filter

    print(type(closed))
    result = closed.finalbid-listings[0].minimum_charge
    return render(request, "auctions/payment.html", {
        "object": closed,
        "coins": coins,
        "address": address,
        "listings": listings[0],
        "total": result})


def pay(request):
    id = request.session['selected_product_id']
    # listingid = request.session['listingid']
    # print("inside pay")
    # for listing in listings:
    #     print(listing)
    #
    # print(address_id)
    try:
        closed = Closebid.objects.filter(id=id, bidder=request.user.username, is_active='Y').first()
    except:
        return redirect('index')
    listing = Listing.objects.filter(id=closed.listingid).first()
    print(listing,'ggggggg',closed.listingid)
    try:
        coins = MyCoin.objects.filter(username = request.user.username).first()
        print(coins.coins_available)
        # print(coins['coins_available'])
    except:
        return redirect('index')

    print(type(closed))
    result = closed.finalbid-listing.minimum_charge
    if coins.coins_available >= result:
        try:
        # if 1==1:
            # Adding transactional row
            transact = add_transaction(username=request.user.username,coins=-result,t_status= 'Y',error=None,cause=f"Bought product {listing.productnames}")
            coins.coins_available = coins.coins_available- result
            coins.save()
            if transact == 0:
                # making update in closed table
                closed.paid_time = now()
                closed.is_active = 'N'
                closed.save()
                print(closed)
                messages.success(request, 'Your Order placed successfully.')
                return orders(request)

            else:
                add_transaction(username=request.user.username,coins=closed.finalbid,t_status= 'N',error="ERROR: Something went wrong in add_transaction.")
                coins.coins_available = coins.coins_available+ closed.finalbid
                coins.save()
        except:
            print("ERROR")
    else:
        messages.error(request, 'Not enough coins.')

    return render(request, "auctions/payment.html", {
        "object": closed,
        "coins": coins})

@login_required()
def orders(request):
    try:
        closed = Closebid.objects.filter(bidder=request.user.username, is_active='N')
    except:
        return redirect('index')

    return render(request, "auctions/orders.html", {
            "object": closed
        })

def download_invoice(request):
    # Create a HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    # Set up the PDF layout here
    p.drawString(100, 750, "Company Name")
    p.drawString(100, 735, "Address Line 1")
    p.drawString(100, 720, "Address Line 2")

    # Add more elements to your billing format...

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response

def transactions_list(request):
    transactions = Transactions.objects.filter(username=request.user.username, t_status='Y').values('coins','entry_at','cause').order_by('-entry_at')  # Order by most recent first
    context = {'transactions': transactions}
    return render(request, 'auctions/transactions_list.html', context)