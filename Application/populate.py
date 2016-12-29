from Application.models import Feed,Item
from Application.rss import read_rss,LINK_ABC,LINK_ELPAIS
from os.path import dirname, join
import datetime

def populate_rss():
    rss,entries = read_rss(LINK_ELPAIS)
    if Feed.objects.filter(title=rss['title'],link=rss['link']).exists():
        feederId = Feed.objects.get(title=rss['title'],link=rss['link']).id
    else:
        feeder = Feed(**rss)
        feeder.save()
        feederId=feeder.id

    for entry in entries:
        itemer = Item(feed_id=feederId, **entry)
        itemer.save()

    pass