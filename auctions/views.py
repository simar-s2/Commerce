from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid, Category
from .forms import CreateListingForm, CommentForm, BidForm


def index(request):
    listings = Listing.objects.all()
    listings_with_prices = []

    for listing in listings:
        bids = Bid.objects.filter(listing=listing)
        highest_bid = bids.last() if bids.exists() else None
        price_to_display = highest_bid.bid if highest_bid else listing.price
        
        listings_with_prices.append({
            "listing": listing,
            "price": price_to_display
        })

    return render(request, "auctions/index.html", {
        "listings": listings_with_prices,
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
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        close_auction = request.POST['close_auction']
        if close_auction == 'true':
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        else: return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


    watchlist = Listing.objects.filter(watchlist=request.user).filter(pk=listing_id)
    comments = Comment.objects.filter(listing=listing_id).all()
    bids = Bid.objects.filter(listing=listing)
    last_bid = bids.last() if bids.exists() else None
    winner = last_bid.user if listing.is_active == False and last_bid != None else None

    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
        "Commentform": CommentForm,
        "Bidform": BidForm,
        "bids": bids,
        "last_bid": last_bid,
        "user": request.user,
        "winner": winner,
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
        if action == 'add':
            listing.watchlist.add(user)
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        elif action == 'remove':
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
            if not bids:
                if form_data['bid'] < listing.price:
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


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def categorical_listings(request, category):
    category_id = Category.objects.get(category=category)
    listings = Listing.objects.filter(category=category_id).all()
    listings_with_prices = []

    for listing in listings:
        bids = Bid.objects.filter(listing=listing)
        highest_bid = bids.last() if bids.exists() else None
        price_to_display = highest_bid.bid if highest_bid else listing.price
        
        listings_with_prices.append({
            "listing": listing,
            "price": price_to_display
        })

    return render(request, "auctions/categorical_listings.html", {
        "listings": listings_with_prices,
        "category": category_id,
    })


@login_required(login_url='/login')
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user).all()
    listings_with_prices = []

    for listing in listings:
        bids = Bid.objects.filter(listing=listing)
        highest_bid = bids.last() if bids.exists() else None
        price_to_display = highest_bid.bid if highest_bid else listing.price
        
        listings_with_prices.append({
            "listing": listing,
            "price": price_to_display
        })

    return render(request, "auctions/my_listings.html", {
        "listings": listings_with_prices,
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
