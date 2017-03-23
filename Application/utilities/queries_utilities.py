from Application.models import Feed,Item,UserProfile

def all_feeds():
    return Feed.objects.all()

def all_feeds_link(user_id=None):
    if user_id == None:
        return Feed.objects.all().values('link')
    else:
        return Feed.objects.all().exclude(users__user_id=user_id).values('link')

def get_feeds_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()

def get_last_items_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()\
        .values('id','title','items__id','items__title','items__description','items__pubDate','items__image')\
        .order_by('-items__pubDate')

def get_item(id):
    return Item.objects.get(id=id)

def get_feed(id):
    return Feed.objects.get(id=id)
