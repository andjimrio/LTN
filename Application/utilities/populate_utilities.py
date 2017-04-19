from Application.models import Feed,Item
from Application.utilities.rss_utilities import read_rss


# Dado un link, parsea el rss y lo convierte a un Feed con sus
#       respectivos Items
def populate_rss(link):
    rss, entries = read_rss(link)
    feeder,bool = Feed.objects.get_or_create(**rss)

    for entry in entries:
        itemer,bool = Item.objects.get_or_create(feed_id=feeder.id, **entry)

    return feeder.id


def update_feed(link, printer=False):
    rss, entries = read_rss(link)
    feeder, bool = Feed.objects.get_or_create(**rss)

    if printer:
        print("\t" + rss['title'])
        cont = 0

    for entry in entries:
        itemer,bool = Item.objects.get_or_create(feed_id=feeder.id, **entry)
        if printer and bool:
            cont += 1

    if printer:
        print('\t\tActualizadas ' + str(cont) + ' entradas.')

    return feeder.id