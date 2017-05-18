from Application.models import UserProfile, Section
from Application.service.profile_services import get_profile


def create_section(title_section, user_id):
    return Section.objects.get_or_create(title=title_section, user=get_profile(user_id))


def get_sections_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).sections.all()


def get_section(section_id):
    return Section.objects.get(id=section_id)


def get_section_items(section_id):
    return Section.objects.get(id=section_id).feeds.all()\
        .values('id', 'title', 'items__id', 'items__title', 'items__description',
                'items__pubDate', 'items__image')\
        .order_by('-items__pubDate')
