from Application.models import Item
from math import log,floor


def get_item_keywords(item_id, len_article):
    keywords = Item.objects.get_keywords('article', item_id, floor(log(len_article)))
    return keywords


def get_item_similarity(item_id):
    more_results = Item.objects.get_more_like_this('article', item_id)
    return more_results


def get_item_query(query):
    results = Item.objects.query('article', query)
    return results
