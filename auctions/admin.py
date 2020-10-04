from django.contrib import admin
from .models import Categorylist, Auctionlist, User, bids, watchlist, comments


# Register your models here.
admin.site.register(Categorylist)
admin.site.register(Auctionlist)
admin.site.register(bids)
admin.site.register(watchlist)
admin.site.register(comments)
