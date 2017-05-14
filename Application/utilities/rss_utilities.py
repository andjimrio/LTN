# encoding: utf-8

import feedparser
from newspaper import Article

from Application.utilities.python_utilities import redo_string, redo_date
from Application.utilities.web_utilitites import clean_html, extract_img_html


def read_rss(link):
    """
    Dado un link, lo parsea y lo convierte y devuelve un diccionario del tipo Feed y una lista de diccionarios del 
    tipo Item  
    :param link: dirección del feed rss 
    :return: un diccionario (feeder) con los datos del Feed y una lista (entries) con los diccionarios de cada noticia
    """
    rss = feedparser.parse(link)
    if rss.entries:
        feeder = {'title':          redo_string(rss.feed, 'title'),
                  'link_rss':       link,
                  'link_web':       redo_string(rss.feed, 'link'),
                  'description':    redo_string(rss.feed, 'description'),
                  'language':       redo_string(rss.feed, 'language'),
                  'logo':           redo_string(rss.feed, 'image', 'href')
                  }

        entries = [get_post(post) for post in rss.entries]

        return feeder, entries
    else:
        return None, None


def get_post(post):
    """
    Dado el diccionario que devuelve rss.entries lo convierte a otro con modelo Item
    
    :param post: diccionario del tipo rss.entries de feedparser
    :return: diccionario del tipo Item
    """
    try:
        article = get_article(post.link)

        top_image = article.top_image
        text = article.text
    except:
        print("ERROR-Article")
        print("\t"+post.title)
        print("\t"+post.link)

    if text == '':
        text = clean_html(redo_string(post, 'description'))

    if top_image == '':
        top_image = extract_img_html(redo_string(post, 'description'))

    entry = {'title': redo_string(post, 'title'),
             'link': redo_string(post, 'link'),
             'description': redo_string(post, 'description'),
             'image': top_image,
             'article': text,
             'creator': redo_string(post, 'author'),
             'pubDate': redo_date(post, 'published')
             }

    return entry


def get_article(link):
    """
    Nos da el objeto Article dado una dirección web
    
    :param link: url de la noticia
    :return: Article de la noticia
    """
    article = Article(link)
    article.download()
    article.parse()
    return article


if __name__ == '__main__':
    LINK_ABC = 'http://www.abc.es/rss/feeds/abcPortada.xml'
    LINK_ELPAIS = 'http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
    LINK_ACEPRENSA = 'http://www.aceprensa.com/rss/'
    LINK_EAL = 'http://feeds.feedburner.com/elandroidelibre'

    #print(feedparser.parse("http://elpais.com/"))
    print(read_rss(LINK_ABC)[0][0].pubDate)