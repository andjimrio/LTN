# encoding: utf-8

import feedparser
from newspaper import Article

from Application.utilities.python_utilities import redo_string,redo_date
from Application.utilities.web_utilitites import clean_html


# Dado un link, lo parsea y lo convierte y devuelve un diccionario del
#       tipo Feed y una lista de diccionarios del tipo Item
def read_rss(link):
    rss = feedparser.parse(link)
    feeder = {'title':          redo_string(rss.feed, 'title'),
              'link_rss':       link,
              'link_web':       redo_string(rss.feed, 'link'),
              'description':    redo_string(rss.feed, 'description'),
              'language':       redo_string(rss.feed, 'language'),
              'logo':           redo_string(rss.feed, 'image', 'href')
              }

    entries = [get_post(post) for post in rss.entries]

    return feeder, entries


# Dado el diccionario que devuelve rss.entries lo convierte a otro
#       con modelo Item
def get_post(post):
    try:
        article = get_article(post.link)

        top_image = article.top_image
        text = article.text
        if text == '':
            text = clean_html(redo_string(post, 'description'))

        entry = {'title':        redo_string(post, 'title'),
                 'link':         redo_string(post, 'link'),
                 'description':  redo_string(post, 'description'),
                 'image':        top_image,
                 'article':      text,
                 'creator':      redo_string(post, 'author'),
                 'pubDate':      redo_date(post, 'published')
                }

        return entry
    except:
        print(post)
        return None




# Descarga y parsea un Article dado un link.
def get_article(link):
    article = Article(link)
    article.download()
    article.parse()
    return article


if __name__ == '__main__':
    LINK_ABC = 'http://www.abc.es/rss/feeds/abcPortada.xml'
    LINK_ELPAIS = 'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
    LINK_ACEPRENSA = 'http://www.aceprensa.com/rss/'

    read_rss(LINK_ELPAIS)[1][0]
    read_rss(LINK_ACEPRENSA)[1][0]
    read_rss(LINK_ABC)[1][0]