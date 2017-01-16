from Application.models import Feed,Item,UserProfile

def all_feeds():
    return Feed.objects.all()

def get_feeds_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).feeds.all()

def get_item(id):
    return Item.objects.get(id=id)