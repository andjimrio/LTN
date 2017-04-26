from Application.models import Feed,Item
from Application.utilities.rss_utilities import read_rss
from Application.utilities.python_utilities import only_keys


# Dado un link, parsea el rss y lo convierte a un Feed con sus
#       respectivos Items
def populate_rss(link):
    rss, entries = read_rss(link)
    feeder,bool = Feed.objects.get_or_create(**rss)

    for entry in entries:
        if not Item.objects.filter(link=entry['link']).exists():
            Item.objects.get_or_create(feed_id=feeder.id, **entry)

    return feeder


def update_feed(link, printer=False):
    rss, entries = read_rss(link)
    feeder, bool = Feed.objects.get_or_create(**rss)

    if printer:
        print("\t" + rss['title'])
        cont = 0

    for entry in entries:
        if not Item.objects.filter(link=entry['link']).exists():
            Item.objects.get_or_create(feed_id=feeder.id, **entry)

            if printer:
                cont += 1

    if printer:
        print('\t\tActualizadas ' + str(cont) + ' entradas.')

    return feeder.id