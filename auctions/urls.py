from django.urls import path
from .views import (
    CategoryListView,
    CommentCreateView,
    ListingListView,
    ListingCreateView,
    ListingDetailView,
    WatchlistListView
)
from . import views

urlpatterns = [
    path("", ListingListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", ListingCreateView.as_view(), name="create-listing"),
    path("listing/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
    path("listing/<int:pk>/watch-item", views.watching_item, name="watch-item"), 
    path("listing/<int:pk>/close-auction", views.close_auction, name="close-auction"),
    path("listing/<int:pk>/leave-a-comment", CommentCreateView.as_view(), name="commenting"),
    path("watchlist",  WatchlistListView.as_view(), name="watchlist"),
    path("categories", views.display_categories, name="display-categories"),
    path("categories/<str:name>/", CategoryListView.as_view(), name="category-items")

]

