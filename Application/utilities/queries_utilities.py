from Application.models import Feed,Item,UserProfile


## SECTIONS

def get_sections_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).sections.all()



## FEEDS

def all_feeds_link(user_id=None):
    if user_id == None:
        return Feed.objects.all().values('link')
    else:
        return Feed.objects.all().exclude(sections__user__user_id=user_id).values('link_rss')








def all_feeds():
    return Feed.objects.all()

def user_has_feed(user_id,feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()

def get_feed_link(link):
    if Feed.objects.filter(link=link).exists():
        return Feed.objects.get(link=link).id
    else:
        return None


def get_feeds_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()

def get_last_items_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).sections.all()\
        .values('feeds__id','feeds__title','feeds__items__id','feeds__items__title',
                'feeds__items__description','feeds__items__pubDate','feeds__items__image')\
        .order_by('-feeds__items__pubDate')

def get_item(id):
    return Item.objects.get(id=id)

def get_feed(id):
    return Feed.objects.get(id=id)

def get_profile(user_id):
    return UserProfile.objects.get(user=user_id)
