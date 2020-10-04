from django.contrib.auth.models import AbstractUser
from django.db import models, migrations


class User(AbstractUser):
    pass


class Categorylist(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Auctionlist(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=150)
    bid = models.PositiveIntegerField()
    category = models.ForeignKey(
        Categorylist, blank=True, on_delete=models.CASCADE, related_name="category")
    image = models.CharField(
        max_length=64, default=None, blank=True, null=True)
    creater = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="user")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}:{self.active} {self.title} {self.description} {self.bid} {self.category} {self.image} {self.creater}"


class bids(models.Model):
    title = models.ForeignKey(
        Auctionlist, on_delete=models.CASCADE, related_name="bidtitle")
    bider = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="biduser")
    otherbid = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bider} {self.otherbid}"


class watchlist(models.Model):
    watchitem = models.ForeignKey(
        Auctionlist, on_delete=models.CASCADE, related_name="watchitem")
    watcher = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="watcher")

    def __str__(self):
        return f"{self.id}:{self.watchitem} {self.watcher}"


class comments(models.Model):
    title = models.ForeignKey(
        Auctionlist, on_delete=models.CASCADE, related_name="commenttitle")
    comment = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.id}:{self.title} {self.comment}"
