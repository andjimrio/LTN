from Application.models import Feed,Item,UserProfile

def all_feeds():
    return Feed.objects.all()

def user_has_feed(user_id,feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()

def get_feed_link(link):
    if Feed.objects.filter(link=link).exists():
        return Feed.objects.get(link=link).id
    else:
        return None

def all_feeds_link(user_id=None):
    if user_id == None:
        return Feed.objects.all().values('link')
    else:
        return Feed.objects.all().exclude(users__user_id=user_id).values('link')

def get_feeds_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()

def exists_feeds_title_by_user(user_id,feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()

def get_last_items_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()\
        .values('id','title','items__id','items__title','items__description','items__pubDate','items__image')\
        .order_by('-items__pubDate')

def get_item(id):
    return Item.objects.get(id=id)

def get_feed(id):
    return Feed.objects.get(id=id)

def get_profile(user_id):
    return UserProfile.objects.get(user=user_id)
