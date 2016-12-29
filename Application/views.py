# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from Application.rss import LINK_ABC,LINK_ELPAIS,LINK_ACEPRENSA
from Application.populate import populate_rss
from Application.queries import all_feeds,get_item
from Application.web import read_main_content

from models import Feed

def home(request):
    return render_to_response('index.html')

def load(request):
    populate_rss(LINK_ELPAIS)
    populate_rss(LINK_ABC)
    populate_rss(LINK_ACEPRENSA)
    return render_to_response('index.html')

def feeds(request):
    feedes = all_feeds()
    return render_to_response('feeds.html',{'feedes':feedes})

def article(request, idItem=None):
    itemer = get_item(idItem)
    link = itemer.link
    web,image = read_main_content(link)
    return render_to_response('article.html',{'link':link,'title':itemer.title,'web':web,'image':image})