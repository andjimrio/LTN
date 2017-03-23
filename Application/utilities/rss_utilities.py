# encoding: utf-8

import feedparser
from bs4 import BeautifulSoup
from dateutil.parser import parse
from django.utils import timezone

from Application.utilities.web_utilitites import get_from_rss

LINK_ABC= 'http://www.abc.es/rss/feeds/abcPortada.xml'
LINK_ELPAIS= 'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
LINK_ACEPRENSA = 'http://www.aceprensa.com/rss/'

def read_rss(link):
    rss = feedparser.parse(link)
    feeder = {'title':rss.feed.title,
              'link':link,
              'description':rss.feed.description,
              'language': redo_string('language',rss.feed)
              }

    entries = [{'title':post.title,
                'link':post.link,
                'description':clean_html(post.description),
                'image':get_from_rss(post.link)[0],
                'article': get_from_rss(post.link)[1],
                'creator': redo_string('author',post),
                'pubDate': redo_date(post)}
               for post in rss.entries]
    return feeder,entries

def redo_string(string, dict):
    if string in dict:
        return dict[string]
    else:
        return ""

def redo_date(post):
    if 'published' in post:
        try:
            return parse(post.published)
        except:
            pass

    return timezone.now()


def clean_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.text


if __name__ == '__main__':
    fecha = read_rss(LINK_ELPAIS)[1][0]['pubDate']
    print(fecha)
    fecha = read_rss(LINK_ACEPRENSA)[1][0]['pubDate']
    print(fecha)
    fecha = read_rss(LINK_ABC)[1][0]['pubDate']
    print(fecha)