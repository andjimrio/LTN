from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from Application.utilities.queries_utilities import get_section, get_section_items


@login_required
def section_view(request, section_id):
    page = request.GET.get('page')

    section = get_section(section_id)

    paginator = Paginator(get_section_items(section_id), 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'section/section_view.html', {'section': section, 'news': news})
