from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from Application.models import UserProfile, Section
from Application.service.profile_services import get_profile


def create_section(title_section, user_id):
    return Section.objects.get_or_create(title=title_section, user=get_profile(user_id))


def get_section(section_id):
    return get_object_or_404(Section, pk=section_id)


def delete_section(section_id, user_id):
    if user_has_section(section_id, user_id):
        Section.objects.get(id=section_id).delete()
        return True
    else:
        raise PermissionDenied


def user_has_section(section_id, user_id):
    return Section.objects.filter(user__user_id=user_id).filter(id=section_id).exists()


def get_sections_by_user(user_id):
    return UserProfile.objects.get(user__id=user_id).sections.all()


def get_section_items(section_id):
    return Section.objects.get(id=section_id).feeds.all()\
        .values('id', 'title', 'items__id', 'items__title', 'items__description',
                'items__pubDate', 'items__image')\
        .order_by('-items__pubDate')
