from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import *



class ListingListView(ListView):
    model = Listing
    template_name = 'auctions/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'listings'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(ListingListView, self).get_context_data(**kwargs)
        context['page'] = "Listings"
        return context


class WatchlistListView(ListView):
    model = Listing
    template_name = 'auctions/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        context = super(WatchlistListView, self).get_context_data(**kwargs)
        context['page'] = "Watchlist"
        return context

    def get_queryset(self):
        watch_list = Watchlist.objects.filter(watcher=self.request.user, watched=True)
        item_list = []

        for item in watch_list:
            i = Listing.objects.get(pk=item.watched_item.pk)
            item_list.append(i)
        return item_list



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
    current_user = request.user
    print(current_user)
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


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'content', 'image', 'min_bid', 'category']

    def get_context_data(self, **kwargs):
        ctx = super(ListingCreateView, self).get_context_data(**kwargs)
        categories = Category.objects.all()

        choices = []

        for category in categories:
            choices.append(category.name)

        ctx['categories'] = choices

        return ctx


    def form_valid(self, form):
        form.instance.seller = self.request.user

        choice = self.request.POST["choices"]
        form.instance.category = Category.objects.get(name=choice)

        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['title', 'comment']

    def form_valid(self, form):
        form.instance.commenter = self.request.user

        item = Listing.objects.get(pk=self.kwargs.get('pk')) #pk se ashtu e kam shenuar tek models kwargs
        form.instance.commented_item = item #look at models' get_abs_url for id

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Comment left successfully')
        return reverse('listing-detail',  kwargs={'pk': self.kwargs.get('pk')})


@method_decorator(login_required, name='post')
class ListingDetailView(DetailView):
    model = Listing

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        user = self.request.user
        item = Listing.objects.get(pk=pk)

        context = super(ListingDetailView, self).get_context_data(**kwargs)

        if str(user) == 'AnonymousUser':
            context['watched'] = False
            return context

        try:
            watching = Watchlist.objects.get(watcher=user, watched_item=item)
            value = watching.watched
        except Watchlist.DoesNotExist:
            value = False

        context['watched'] = value

        if user == item.seller:
            context['closed'] = True

        if Winner.objects.filter(winner=user, won_item=item).exists():
            messages.add_message(self.request, messages.SUCCESS, "Congrats. You have won the auction!")

        if Comment.objects.filter(commented_item=item).exists():
            context["comments"] = Comment.objects.filter(commented_item=item).order_by('-date_posted').all()
         
        return context


    def post(self, request, pk):
        user = request.user
        bidder = User.objects.filter(username=user)
        #float error when not float
        new_bid = float(request.POST["user_bid"])
        item = Listing.objects.get(pk=pk)

        bid = Bid.objects.filter(listed_item=pk).order_by('-bid').first()

        if bid is None:
            highest_bid = item.min_bid
        else:
            highest_bid = bid.bid

        if new_bid < highest_bid:
            messages.add_message(request, messages.WARNING, "Bid is too low.")

        else:

            try:
                bid = Bid.objects.get(listed_item=item, bidder=user)
                bid.bid = new_bid
                bid.save()

            except Bid.DoesNotExist:
                b = Bid.objects.create(bid=new_bid, listed_item=item)
                b.bidder.set(bidder)

            item.min_bid = new_bid
            item.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Bid placed successfully.")

        return redirect('listing-detail', self.kwargs['pk'])


@login_required(login_url='login')
def watching_item(request, pk):
    item = Listing.objects.get(pk=pk)
    user = request.user
    watcher = User.objects.filter(username=user)

    try:
        watching = Watchlist.objects.get(
            watcher=user, watched_item=item)  # filter by list item too
        watching.watched = not (watching.watched)
        watching.save()

        if watching.watched:
            messages.add_message(request, messages.SUCCESS,
                                 "Item added successfully.")
        else:
            messages.add_message(request, messages.SUCCESS,
                                 "Item removed successfully.")

    except Watchlist.DoesNotExist:

        w = Watchlist.objects.create(watched=True, watched_item=item)
        w.watcher.set(watcher)

        messages.add_message(request, messages.SUCCESS,
                             "Item added successfully.")

    return redirect('listing-detail', pk)


@login_required(login_url='login')
def close_auction(request, pk):

    item = get_object_or_404(Listing, pk=pk)
    item.ended = True
    item.save() 

    won = Bid.objects.filter(listed_item=item).order_by('-bid').first() 

    if won is not None:

        for username in won.bidder.all():
            winner = username

        winner = User.objects.get(username=winner)
        w = Winner(winner=winner, won_item=item)
        w.save()

    return redirect('listing-detail', pk)


def display_categories(request):

    context = {
        "categories" : Category.objects.all()
    }

    return render(request, "auctions/categories.html", context)


class CategoryListView(ListView):
    model = Listing
    template_name = 'auctions/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        mydict = self.kwargs
        name = mydict["name"]

        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['page'] = 'Category: ' + name
        return context

    def get_queryset(self):
        mydict = self.kwargs
        name = mydict["name"]
        
        category = Category.objects.get(name=name)

        if name == 'Others':
            items = Listing.objects.filter(Q(category=category) | Q(category__isnull=True)).all()
        else:
            items = Listing.objects.filter(category=category).all() 

        item_list = []

        for item in items:
            i = Listing.objects.get(id=item.id)
            item_list.append(i)
        return item_list