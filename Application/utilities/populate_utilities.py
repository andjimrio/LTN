from Application.models import Feed,Item
from Application.utilities.rss_utilities import read_rss


def populate_rss(link, printer=False):
    rss, entries = read_rss(link)
    if Feed.objects.filter(title=rss['title'],link=rss['link']).exists():
        feederId = Feed.objects.get(title=rss['title'],link=rss['link']).id
    else:
        feeder = Feed(**rss)
        feeder.save()
        feederId=feeder.id

    if printer:
        print("\t"+rss['title'])
        cont = 0

    for entry in entries:
        if not Item.objects.filter(feed_id=feederId,title=entry['title']).exists():
            itemer = Item(feed_id=feederId, **entry)
            itemer.save()
            if printer:
                cont += 1

    if printer:
        print('\t\tActualizadas ' + str(cont) + ' entradas.')

    return feederId