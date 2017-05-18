from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Application.services import get_pagination
from Application.service.section_services import get_section, get_section_items


@login_required
def section_view(request, section_id):
    section = get_section(section_id)
    news = get_pagination(request.GET.get('page'), get_section_items(section_id))

    return render(request, 'section/section_view.html', {'section': section, 'news': news})
