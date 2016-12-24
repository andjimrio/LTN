from Application.models import Feed,Item
from Application.rss import read_rss,LINK_ABC
from os.path import dirname, join
import datetime

def populate_rss():
    Feed.objects.filter().delete()

    rss,entries = read_rss(LINK_ABC)
    feeder = Feed(**rss)
    feeder.save()

    for entry in entries:
        itemer = Item(feed_id=feeder.id, **entry)
        itemer.save()

    pass