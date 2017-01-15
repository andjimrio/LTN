from Application.models import Feed,Item
from Application.rss import read_rss

def populate_rss(link):
    rss,entries = read_rss(link)
    if Feed.objects.filter(title=rss['title'],link=rss['link']).exists():
        feederId = Feed.objects.get(title=rss['title'],link=rss['link']).id
    else:
        feeder = Feed(**rss)
        feeder.save()
        feederId=feeder.id

    for entry in entries:
        if not Item.objects.filter(feed_id=feederId,title=entry['title']).exists():
            itemer = Item(feed_id=feederId, **entry)
            itemer.save()

    return feederId