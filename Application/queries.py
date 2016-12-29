from Application.models import Feed,Item

def all_feeds():
    return Feed.objects.all()

def get_item(id):
    return Item.objects.get(id=id)