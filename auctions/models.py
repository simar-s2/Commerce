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
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(verbose_name="date created", auto_now_add=True)

    def __str__(self):
        return(f"{self.title}")

# class Bid(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE)
#     bid = models.IntegerField(max_length=10, null=False)

#     def __str__(self):
#         return(f"{self.bidder} made a bid of {self.bid} on {self.listing}")