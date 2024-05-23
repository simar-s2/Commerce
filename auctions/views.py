from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Comment, Bid, Category
from .forms import CreateListingForm, CommentForm, BidForm

# Function that attempts to get listings based on a queryset
def get_listings(query: QuerySet) -> list:
    listings = Listing.objects.filter(query)
    listings_with_prices = []

    for listing in listings:
        # Checking for the highest bid else selecting price
        bids = Bid.objects.filter(listing=listing)
        highest_bid = bids.last() if bids.exists() else None
        price_to_display = highest_bid.bid if highest_bid else listing.price
        
        listings_with_prices.append({
            "listing": listing,
            "price": price_to_display
        })
    
    # Returning list of listings with highest bid or starting price
    return listings_with_prices


def index(request):
    # Querying all listings
    query = Q()
    listings = get_listings(query)

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        # Checking if form is valid
        if form.is_valid():
            form_data = form.cleaned_data
            owner = User.objects.filter()
            if form_data['price'] < 0:
                messages.error(request, 'Price cannot be negative!')
                return HttpResponseRedirect(reverse("index"))
            # Creating listing
            listing = Listing(
                title=form_data['title'],
                description=form_data['description'],
                image=form_data['image'],
                price=form_data['price'],
                owner=request.user,
                category=form_data['category']
                )
            # Attempt to save listing
            try:
                listing.save()
                messages.success(request, 'Listing Created!')
                return HttpResponseRedirect(reverse("index"))
            # Error
            except:
                messages.error(request, 'Error in creating listing!')
                return HttpResponseRedirect(reverse("index"))
        messages.error(request, 'Error in creating listing!')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm,
        })


@login_required(login_url='/login')
def view_listing(request, listing_id):
    # Attempt to query listing
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        # Try close auction
        close_auction = request.POST['close_auction']
        if close_auction == 'true':
            listing.is_active = False
            listing.save()
            messages.success(request, 'Auction closed!')
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        # Error
        else: 
            messages.success(request, 'Error closing auction!')
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


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
    # Query listings in users watchlist
    query = Q(watchlist=request.user)
    listings = get_listings(query)

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })


@login_required(login_url='/login')
def add_remove_watchlist(request, listing_id):
    if request.method == "POST":
        action = request.POST['action']
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        # Try to add to watchlist
        if action == 'add':
            listing.watchlist.add(user)
            messages.success(request, 'Added to watchlist!')
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        # Try to remove from watchlist
        elif action == 'remove':
            listing.watchlist.remove(user)
            messages.success(request, 'Removed from watchlist!')
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
        # Error
        else:
            messages.success(request, 'An error occured, please try again!')
            return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


@login_required(login_url='/login')
def add_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        # Check if form is valid
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
        # Check if form is valid
        if form.is_valid():
            form_data = form.cleaned_data
            if not bids:
                # Checking if bid is valid
                if form_data['bid'] < listing.price:
                    messages.error(request, 'Bid cannot be lower than the asking price!')
                    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
                # Adding bid
                else:
                    messages.success(request, 'Bid placed!')
                    bid = Bid(user=user, listing=listing, bid=form_data['bid'])
                    bid.save()
            else:
                # Checking if bid is valid
                if form_data['bid'] <= bids.last().bid: 
                    messages.error(request, 'Bid must be higher than the last bid!')
                    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))
                # Adding bid
                else:
                    messages.success(request, 'Bid placed!')
                    bid = Bid(user=user, listing=listing, bid=form_data['bid'])
                    bid.save()
    return HttpResponseRedirect(reverse('view_listing', args=(listing_id, )))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def categorical_listings(request, category_name):
    # Attempt to query listings according to the category
    category = get_object_or_404(Category, category=category_name)
    query = Q(category=category)
    listings = get_listings(query)

    return render(request, "auctions/categorical_listings.html", {
        "listings": listings,
        "category": category,
    })


@login_required(login_url='/login')
def my_listings(request):
    # Query listings owned by user
    query = Q(owner=request.user)
    listings = get_listings(query)
    
    return render(request, "auctions/my_listings.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if all required fields are not empty
        if not username or not password:
            messages.error(request, 'Please fill in all fields')
            return HttpResponseRedirect(reverse("index"))

        # Attempt to sign user in
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully!')
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, 'Incorrect username or password!')
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        # Check if all required fields are not empty
        if not username or not password or not confirmation:
            messages.error(request, 'Please fill in all the required fields!')
            return HttpResponseRedirect(reverse("register"))

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, 'Password do not match!')
            return HttpResponseRedirect(reverse("register"))

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, 'Username already taken!')
            return HttpResponseRedirect(reverse("register"))
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
