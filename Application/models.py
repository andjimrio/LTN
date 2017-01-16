#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    pass

class Item(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    pubDate = models.DateTimeField()
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.title

    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    feeds = models.ManyToManyField(Feed, related_name="users")

    def __str__(self):
        return self.user.username
