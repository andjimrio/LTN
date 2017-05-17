from django.utils import timezone
from django.db.models import Count, Q

from Application.models import Feed, Item, UserProfile, Section,\
    Status, Keyword


# USERPROFILE

def all_profile():
    return UserProfile.objects.all()


def get_profile(user_id):
    return UserProfile.objects.get(user=user_id)


# SECTIONS

def get_sections_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).sections.all()


def get_section(section_id):
    return Section.objects.get(id=section_id)


# FEEDS

def all_feeds_link(user_id=None):
    if user_id is None:
        return Feed.objects.all().values('link_rss')
    else:
        return Feed.objects.all().exclude(sections__user__user_id=user_id).values('link_rss')


def get_feeds_by_user(user_id):
    return Feed.objects.filter(sections__user__user_id=user_id).all()


def user_has_feed(user_id,feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()


def get_feed(feed_id):
    return Feed.objects.get(id=feed_id)


def get_feed_id_by_link(link_rss):
    return Feed.objects.get(link_rss=link_rss).id


# ITEM

def get_item(item_id):
    return Item.objects.get(id=item_id)


def get_last_items_by_user(user_id, unview=False):
    if unview:
        return UserProfile.objects.get(user__id=user_id).sections.all()\
            .values('feeds__id','feeds__title','feeds__items__id','feeds__items__title',
                    'feeds__items__description','feeds__items__pubDate','feeds__items__image')\
            .order_by('-feeds__items__pubDate')
    else:
        return UserProfile.objects.get(user__id=user_id).statuses.all().\
            filter(view=False).\
            values('item__feed_id','item__feed__title','item_id','item__title',
                   'item__description','item__pubDate','item__image').\
            order_by('-item__pubDate')


def get_item_today_by_section(section_id):
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=1)
    return Section.objects.filter(id=section_id).filter(feeds__items__pubDate__range=[start_date, end_date])\
        .values('feeds__items__id','feeds__items__title')


# STATUS

def get_status_by_user_item(user_id, item_id):
    return Status.objects.get(user_id=get_profile(user_id).id,item_id=item_id)


def get_filtered_status_by_profile(profile_id):
    return Status.objects.filter(user_id=profile_id).filter(read=True)\
        .union(Status.objects.filter(user_id=profile_id).filter(like=True))


def get_status_read_stats_by_user(profile_id):
    return Status.objects.filter(user_id=profile_id, view=True) \
        .values('item__feed__sections__title')\
        .annotate(total=Count('id'))


def get_status_like_stats_by_user(profile_id):
    return Status.objects.filter(user_id=profile_id, like=True) \
        .values('item__feed__sections__title')\
        .annotate(total=Count('id'))


# KEYWORDS

def get_keywords_by_user(user_id):
    return Keyword.objects.filter(users__user=user_id).all()


