from Application.models import Feed


def create_feed(**dict_feed):
    return Feed.objects.get_or_create(**dict_feed)


def get_feed(feed_id):
    return Feed.objects.get(id=feed_id)


def get_section_by_feed(feed_id, user_id):
    return Feed.objects.get(id=feed_id).sections.all().get(user__user_id=user_id)


def all_feeds_link(user_id=None):
    if user_id is None:
        return Feed.objects.all().values('link_rss')
    else:
        return Feed.objects.all().exclude(sections__user__user_id=user_id).values('link_rss')


def get_feeds_by_user(user_id):
    return Feed.objects.filter(sections__user__user_id=user_id).all()


def user_has_feed(user_id, feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()


def exists_feed_id_by_link(link_rss):
    return Feed.objects.filter(link_rss=link_rss).exists()


def get_feed_by_link(link_rss):
    return Feed.objects.get(link_rss=link_rss)

