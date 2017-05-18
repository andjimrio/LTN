from Application.models import Feed, Item
from Application.service.feed_services import get_feed_id_by_link, create_feed
from Application.service.section_services import create_section
from Application.utilities.rss_utilities import read_rss


def populate_rss(link, title_section, user_id):
    rss, entries = read_rss(link)
    if rss:
        feeder = create_feed(**rss)[0]
        section = create_section(title_section, user_id)[0]
        feeder.sections.add(section)
        feeder.save()

        for entry in entries:
            if entry and not Item.objects.filter(link=entry['link']).exists():
                Item.objects.get_or_create(feed_id=feeder.id, **entry)

        return feeder
    else:
        return None


def update_feed(link, printer=False):
    rss, entries = read_rss(link)
    feed_id = get_feed_id_by_link(link)

    if printer:
        print("\t" + rss['title'])
        cont = 0

    for entry in entries:
        if not Item.objects.filter(link=entry['link']).exists():
            Item.objects.get_or_create(feed_id=feed_id, **entry)

            if printer:
                cont += 1

    if printer:
        print('\t\tActualizadas ' + str(cont) + ' entradas.')

    return feed_id
