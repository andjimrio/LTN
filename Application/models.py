#encoding:utf-8
from django.db import models

# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    language = models.CharField(max_length=50)
    pubDate = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title

    pass

class Item(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    pubDate = models.CharField(max_length=500)
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="items")

    def __unicode__(self):
        return self.title

    pass