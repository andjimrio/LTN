import kronos
from Application.populate import populate_rss
from Application.queries import all_feeds_link


@kronos.register('0 * * * *')
def cron_populate_rss():
    for line in all_feeds_link():
        populate_rss(line['link'])