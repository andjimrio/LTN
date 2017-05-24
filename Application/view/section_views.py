from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Application.models import Section
from Application.forms import SectionForm
from Application.services import get_pagination
from Application.service.section_services import get_section_items


@login_required
def section_view(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    news = get_pagination(request.GET.get('page'), get_section_items(section_id))

    return render(request, 'section/section_view.html', {'section': section, 'news': news})


@login_required
def section_edit(request, section_id):
    section = get_object_or_404(Section, pk=section_id)

    section_form = SectionForm(request.POST or None, instance=section)

    if section_form.is_valid():
        section_form.save()
        return redirect('section_view', section_id=section_id)
    else:
        print(section_form.errors)

    return render(request, 'section/section_edit.html', {'section_form': section_form, 'section_id': section.id})


@login_required
def section_delete(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    section.delete()

    return redirect('feed_list')
