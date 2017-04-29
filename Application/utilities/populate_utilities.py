from Application.models import Feed,Item,Section
from Application.utilities.queries_utilities import get_profile
from Application.utilities.rss_utilities import read_rss


# Dado un link, parsea el rss y lo convierte a un Feed con sus
#       respectivos Items
def populate_rss(link,title_section,user_id):
    rss, entries = read_rss(link)
    feeder,bool = Feed.objects.get_or_create(**rss)
    section, cond = Section.objects.get_or_create(title=title_section,
                                                  user=get_profile(user_id))
    feeder.sections.add(section)
    feeder.save()

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