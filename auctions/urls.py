from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("eachlists/<int:listnumber>", views.eachlists, name="eachlists"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("categorylist", views.categorylist, name="categorylist"),
    path("categorylist/<int:categorylist_item>",
         views.categoryitem, name="categoryitem"),
    path("watchlist/<int:userid>", views.watchlists, name="watchlist")
]
