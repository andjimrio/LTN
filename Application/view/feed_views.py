from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Application.forms import FeedForm
from Application.utilities.populate_utilities import populate_rss
from Application.services import get_pagination
from Application.service.feed_services import get_feed, all_feeds_link, user_has_feed
from Application.service.section_services import get_sections_by_user, get_section


@login_required
def feed_create(request):
    error = False

    if request.method == 'POST':
        feed_form = FeedForm(request.POST)

        if feed_form.is_valid():
            url = feed_form.data['url']
            title_section = feed_form.data['section']

            feed = populate_rss(url, title_section, request.user.id)

            if feed:
                return redirect('feed_list')
            else:
                error = True

        else:
            print(feed_form.errors)

    else:
        feed_form = FeedForm()

    urls = all_feeds_link(request.user.id)
    sections = get_sections_by_user(request.user.id)

    return render(request, 'feed/feed_create.html',
                  {'feed_form': feed_form, 'error': error, 'urls': urls, 'sections': sections})


@login_required
def feed_view(request, feed_id):
    feeder = get_feed(feed_id)
    news = get_pagination(request.GET.get('page'), feeder.items.all())

    return render(request, 'feed/feed_view.html', {'feed': feeder, 'news': news})


@login_required
def feed_list(request):
    sections = get_sections_by_user(request.user.id)
    return render(request, 'feed/feed_list.html', {'sections': sections})


@login_required
def feed_delete(request, section_id, feed_id):
    if user_has_feed(request.user.id, feed_id):
        section = get_section(section_id)
        section.feeds.remove(get_feed(feed_id))
        section.save()

    return redirect('feed_list')
