# encoding: utf-8

import feedparser
from bs4 import BeautifulSoup

LINK_ABC= 'http://www.abc.es/rss/feeds/abcPortada.xml'

def read_rss(link):
    rss = feedparser.parse(link)
    feeder = {'title':rss.feed.title,
              'link':rss.feed.link,
              'description':rss.feed.description,
              'language':rss.feed.language}

    entries = [{'title':post.title,
                'link':post.link,
                'description':clean_html(post.description),
                'pubDate':post.published}
               for post in rss.entries]
    return feeder,entries


def clean_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.text


if __name__ == '__main__':
    print read_rss(LINK_ABC)[0]