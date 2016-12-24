from Application.models import Feed

def all_feeds():
    return Feed.objects.all()