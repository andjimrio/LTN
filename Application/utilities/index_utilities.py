from Application.models import Item
from Application.utilities.queries_utilities import get_keywords_by_user


def get_item_keywords(item_id, num_terms):
    keywords = Item.objects.get_keywords('article', item_id, num_terms)
    return keywords


def get_item_similarity(item_id):
    more_results = Item.objects.get_more_like_this('article', item_id)
    return more_results


def get_item_query(query):
    results = Item.objects.query('article', query)
    return results


def get_item_recommend(user_id):
    keys_user = get_keywords_by_user(user_id)
    results = Item.objects.query('article', " OR ".join([x.term for x in keys_user]))\
        .filter(statuses__user__user_id=user_id)\
        .exclude(statuses__view=True)\
        .order_by('-pubDate')
    return results
