from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auctionlist, Categorylist, bids, watchlist, comments
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def index(request):
    return render(request, "auctions/index.html", {
        "thenewlist": Auctionlist.objects.filter(active=True)
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
        return render(request, "auctions/register.html",)


@login_required
def createlist(request):
    items = Categorylist.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        # get the data of new list
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        category = Categorylist.objects.get(name=request.POST["category"])
        imageurl = request.POST["imageurl"]
        creater = User.objects.get(username=username)
        thenewlist = Auctionlist(
            title=title, description=description, bid=bid, category=category, image=imageurl, creater=creater)
        thenewlist.save()
        return render(request, "auctions/index.html", {
            "thenewlist": Auctionlist.objects.all()})
    else:
        return render(request, "auctions/createlist.html", {
            "selectitem": items,
            "name": username
        })


def categorylist(request):
    items = Categorylist.objects.all()
    return render(request, "auctions/categorylist.html", {
        "categorylist": Categorylist.objects.all()
    })


def categoryitem(request, categorylist_item):
    items = Auctionlist.objects.filter(category=categorylist_item)
    return render(request, "auctions/categorylist.html", {
        "categoryitem": items
    })


@login_required
def eachlists(request, listnumber):
    thelist = Auctionlist.objects.get(pk=listnumber)
    bid = bids.objects.filter(title=thelist).order_by('-otherbid')[:1]
    bidnumber = bids.objects.filter(title=thelist).count()
    # bid = bids.objects.filter(title=thelist).order_by('-otherbid').first()
    if thelist.active == True:
        if request.method == "POST":
            # for bid post
            if 'addbid' in request.POST:
                otherbid = request.POST["otherbid"]
                title = Auctionlist.objects.get(title=thelist.title)
                bider = User.objects.get(username=request.user.username)
                if int(otherbid) > int(thelist.bid):
                    thenewbid = bids(title=title, bider=bider,
                                     otherbid=otherbid)
                    thenewbid.save()
                    bidnumber = bids.objects.filter(title=thelist).count()
                    return render(request, "auctions/eachlists.html", {
                        "bider": bids.objects.all(),
                        "thelist": thelist,
                        "bidnumber": bidnumber,
                        "commentlist": comments.objects.filter(title=thelist)
                    })
                else:
                    return render(request, "auctions/eachlists.html", {
                        "errorhint": "the bid should bigger than the current",
                        "thelist": thelist,
                        "commentlist": comments.objects.filter(title=thelist),
                        "bidnumber": bidnumber
                    })
            # close active
            elif 'active' in request.POST:
                #  if you are the creater could close other couldnt
                if thelist.creater.username == request.user.username:
                    thelist.active = False
                    thelist.save()

                    return render(request, "auctions/eachlists.html", {
                        "thelist": thelist,
                        "commentlist": comments.objects.filter(title=thelist),
                        "noactive": "You have close this page successfully"
                    })
                else:
                    return render(request, "auctions/eachlists.html", {
                        "thelist": thelist,
                        "commentlist": comments.objects.filter(title=thelist),
                        "noactive": "You dont gave the right to close the page"
                    })
            # else for comment post
            else:
                title = Auctionlist.objects.get(title=thelist.title)
                thecomment = request.POST["newcomment"]
                newcomment = comments(title=title, comment=thecomment)
                newcomment.save()
                return render(request, "auctions/eachlists.html", {
                    "thelist": thelist,
                    "commentlist": comments.objects.filter(title=title),
                    "bidnumber": bidnumber
                })
        else:
            return render(request, "auctions/eachlists.html", {
                "thelist": thelist,
                "commentlist": comments.objects.filter(title=thelist),
                "bidnumber": bidnumber
            })
    else:
        return render(request, "auctions/eachlists.html", {
            "thelist": thelist,
            "commentlist": comments.objects.filter(title=thelist),
            "owner": "This page already closed",
            "won": "won this auction",
            "bidwinner": bid
        })


@login_required
def watchlists(request, userid):
    watcher = User.objects.get(pk=userid)  # ONLY USERNAME
    if request.method == "POST":
        watchitemid = request.POST["itemid"]
        watchitem = Auctionlist.objects.get(pk=watchitemid)
        newwatchlist = watchlist(watchitem=watchitem, watcher=watcher)
        newwatchlist.save()
        return render(request, "auctions/watchlist.html", {
            "watch": watchlist.objects.filter(watcher=watcher)
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "watch": watchlist.objects.filter(watcher=watcher)
        })
