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
    path("add_remove_watchlist/<int:listing_id>", views.add_remove_watchlist, name="add_remove_watchlist")
]
