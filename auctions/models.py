from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=130, unique=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100, default=None, blank=False)
    image = models.ImageField(blank=True, upload_to='media', default="noimage.jpg")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE) ##
    min_bid = models.FloatField(blank=False, validators=[MinValueValidator(0)])
    ended = models.BooleanField(default=False)

    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(300, 150)], format='JPEG', options={'quality':100})
    image_thumbnail1 = ImageSpecField(source='image', processors=[ResizeToFill(1200, 500)], format='JPEG', options={'quality':100})

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})


class Bid(models.Model):
    bid = models.FloatField(validators=[MinValueValidator(0)])
    bidder = models.ManyToManyField(User, default=None)
    listed_item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)

    #def get_absolute_url(self):
     #   return reverse('listing-detail', kwargs={'pk': self.pk})


class Watchlist(models.Model):
    watched = models.BooleanField(default=False)
    watcher = models.ManyToManyField(User, default=None) 
    watched_item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)


class Winner(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 
    won_item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)


class Comment(models.Model):
    title = models.CharField(blank=False, max_length= 150, default=None)
    comment =  models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    commented_item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None) 


    def get_absolute_url(self):
        return reverse('commenting', kwargs={'pk': self.pk})
