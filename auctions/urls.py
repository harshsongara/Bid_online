from django.urls import path
# from django.conf.urls import url, include
# from django.urls import include, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createlisting, name="create"),
    path("category", views.category, name="category"),
    path("listing/<int:id>", views.listingpage, name="listingpage"),
    path("listing/<int:id>/addwatch",views.addwatch,name="addwatch"),
    path("listing/<int:id>/removewatch",views.removewatch,name="removewatch"),
    path("listing/<int:listingid>/bid",views.bid,name="bid"),
    path("listing/<int:listingid>/closebid",views.closebid,name="closebid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listingid>/closed", views.closed, name="closed"),
    path("comment/<int:listingid>", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<str:cats>", views.categorylistings, name="categorylistings"),   
    path("listing/closed", views.allclosed, name="allclosed"),
    path("coin", views.coin, name="coin"),
    path("coin/add", views.addCoin, name="addCoin"),
    path("coin/transactions", views.transactions_list, name="transactions_list"),
    path("select_address", views.selectAddress, name="selectAddress"),
    path("address", views.address, name="address"),
    path("address/add", views.addAddress, name="addAddress"),
    path("pay", views.pay, name="pay"),
    path("orders", views.orders, name="orders"),
    path('orders/invoice', views.download_invoice, name='download_invoice')
]
