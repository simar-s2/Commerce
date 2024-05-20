from django.contrib import admin
from .models import Listing, User, Comment, Bid, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Category)
