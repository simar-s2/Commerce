from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid
from .forms import CreateListingForm, CommentForm, BidForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            owner = User.objects.filter()
            listing = Listing(
                title=form_data['title'],
                description=form_data['description'],
                image=form_data['image'],
                price=form_data['price'],
                owner=request.user,
                category=form_data['category']
                )
            listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm,
        })


@login_required(login_url='/login')
def view_listing(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id).first()
    watchlist = Listing.objects.filter(watchlist=request.user).filter(pk=listing_id)
    comments = Comment.objects.filter(listing=listing_id).all()
    bids = Bid.objects.filter(listing=listing)
    last_bid = bids.last() if bids.exists() else None
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
        "Commentform": CommentForm,
        "Bidform": BidForm,
        "bids": bids,
        "last_bid": last_bid,
        "user": request.user,
    })


@login_required(login_url='/login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(watchlist=request.user)
    })


@login_required(login_url='/login')
def add_remove_watchlist(request, listing_id):
    if request.method == "POST":
        action = request.POST['action']
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        if action == 'Add to watchlist':
            listing.watchlist.add(user)
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        elif action == 'Remove from watchlist':
            listing.watchlist.remove(user)
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        else:
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


@login_required(login_url='/login')
def add_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        if form.is_valid():
            form_data = form.cleaned_data
            comment = Comment(user=request.user, listing=listing, comment=form_data['comment'])
            comment.save()

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id, )))


@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(listing=listing).all()
        if form.is_valid():
            form_data = form.cleaned_data
            # If first bid does not exist, check the listing price and make sure the bid is greater or equal
            if not bids:
                if float(form_data['bid']) < float(listing.price):
                    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
                else:
                    bid = Bid(user=user, listing=listing, bid=form_data['bid'])
                    bid.save()
            else:
                last_bid = bids[len(bids) - 1]
                if form_data['bid'] <= last_bid.bid:
                    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
                else:
                    bid = Bid(user=user, listing=listing, bid=form_data['bid'])
                    bid.save()
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


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
