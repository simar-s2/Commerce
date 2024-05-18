from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return(f"{self.username}")

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.CharField(verbose_name="image url", max_length=500, blank=True)
    price = models.FloatField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return(f"{self.title}")

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    
    def __str__(self):
        return(f"{self.user} made a bid of {self.bid} on {self.listing}")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentor")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    comment = models.CharField(max_length=300)
    date = models.DateTimeField(verbose_name="date created", auto_now_add=True)

    def __str__(self):
        return(f"{self.user} commented {self.comment}")
