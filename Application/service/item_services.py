from collections import Counter

from django.utils import timezone

from Application.models import Item, UserProfile, Section, Status
from Application.utilities.python_utilities import floor_log
from Application.service.profile_services import get_profile, get_keywords_by_user


def create_item(**dict_item):
    return Item.objects.get_or_create(**dict_item)


def get_item(item_id):
    return Item.objects.get(id=item_id)


def exists_item_by_link(link):
    return Item.objects.filter(link=link).exists()


def get_status_by_user_item(user_id, item_id):
    return Status.objects.get_or_create(user_id=get_profile(user_id).id, item_id=item_id)


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


class SectionSummaryKeywords:
    def __init__(self, section_title):
        self.section = section_title
        self.keywords_counters = dict()
        self.counts_counters = Counter()

    def add_keyword(self, keywords, item_id, item_title):
        exists = False
        keyword = keywords[0]

        for key in keywords:
            if key in self.keywords_counters:
                exists = True
                keyword = key
                break

        if exists:
            self.keywords_counters[keyword].update(item_id, item_title)
        else:
            keyword_counter = KeywordCounter(keyword, item_id, item_title)
            self.keywords_counters[keyword] = keyword_counter

        self.counts_counters[keyword] += 1

    def most_common(self, number=None):
        if not number and self.counts_counters:
            number = floor_log(len(self.counts_counters))
        else:
            number = 0
        return [self.keywords_counters[keyword[0]] for keyword in self.counts_counters.most_common(number)]

    def __str__(self):
        return "SSK: {} - {}".format(self.section, len(self.keywords_counters))


class KeywordCounter:
    def __init__(self, keyword, item_id, item_title):
        self.keyword = keyword
        self.counts = 1
        self.sample_title = item_title
        self.items = dict()
        self.items[item_id] = item_title

    def update(self, item_id, item_title):
        self.counts += 1
        self.items[item_id] = item_title

    def __str__(self):
        return "KC: {} - {}".format(self.keyword, self.counts)