# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from Application.populate import populate_rss
from Application.queries import all_feeds

from models import Feed

def home(request):
    return render_to_response('index.html')

def load(request):
    populate_rss()
    return render_to_response('index.html')

def feeds(request):
    feed = all_feeds()[0]
    return render_to_response('feeds.html',{'feed':feed})