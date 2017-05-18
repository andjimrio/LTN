from django.utils import timezone

from Application.models import Item, UserProfile, Section, Status
from Application.service.profile_services import get_profile, get_keywords_by_user


def get_item(item_id):
    return Item.objects.get(id=item_id)


def get_status_by_user_item(user_id, item_id):
    return Status.objects.get(user_id=get_profile(user_id).id, item_id=item_id)


def get_last_items_by_user(user_id, unview=False):
    if unview:
        return UserProfile.objects.get(user__id=user_id).sections.all()\
            .values('feeds__id', 'feeds__title', 'feeds__items__id', 'feeds__items__title',
                    'feeds__items__description', 'feeds__items__pubDate', 'feeds__items__image')\
            .order_by('-feeds__items__pubDate')
    else:
        return UserProfile.objects.get(user__id=user_id).statuses.all().\
            filter(view=False).\
            values('item__feed_id', 'item__feed__title', 'item_id', 'item__title',
                   'item__description', 'item__pubDate', 'item__image').\
            order_by('-item__pubDate')


def get_item_today_by_section(section_id):
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=1)
    return Section.objects.filter(id=section_id).filter(feeds__items__pubDate__range=[start_date, end_date])\
        .values('feeds__items__id', 'feeds__items__title')


def get_item_keywords(item_id, num_terms):
    keywords = Item.objects.get_keywords('article', item_id, num_terms)
    return keywords


def get_item_similarity(item_id, limit):
    more_results = Item.objects.get_more_like_this('article', item_id, limit)
    return more_results


def get_item_query(query):
    results = Item.objects.query('article', query)
    return results


def query_multifield_dict(dict_query):
    results = Item.objects.query_multifield_dict(dict_query)
    return results


def get_item_recommend(user_id):
    keys_user = [x.term for x in get_keywords_by_user(user_id)]
    results = Item.objects.query_list_or('article', keys_user)\
        .filter(statuses__user__user_id=user_id)\
        .exclude(statuses__view=True)\
        .order_by('-pubDate')
    return results
