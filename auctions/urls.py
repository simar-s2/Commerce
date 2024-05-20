from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("view_listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_remove_watchlist/<int:listing_id>", views.add_remove_watchlist, name="add_remove_watchlist"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("listings/<category>", views.categorical_listings, name="listings"),
    path("my_listings", views.my_listings, name="my_listings")
]
