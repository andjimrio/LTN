from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect

from Application.forms import FeedForm
from Application.models import Feed,Section
from Application.utilities.populate_utilities import populate_rss
from Application.utilities.queries_utilities import get_feeds_by_user,get_feed,all_feeds_link,\
    user_has_feed,get_profile,get_sections_by_user,get_section

@login_required
def feed_create(request):
    error = False

    if request.method == 'POST':
        feed_form = FeedForm(request.POST)

        if feed_form.is_valid():
            profile = get_profile(request.user)
            url = feed_form.data['url']
            title_section = feed_form.data['section']
            section, cond = Section.objects.get_or_create(title=title_section,
                                                          user=get_profile(request.user.id))

            feed = populate_rss(url)
            feed.sections.add(section)
            feed.save()

            return redirect('feed_list')

        else:
            print(feed_form.errors)

    else:
        feed_form = FeedForm()

    urls = all_feeds_link(request.user.id)
    sections = get_sections_by_user(request.user.id)

    return render(request, 'feed/feed_create.html',
                  {'feed_form':feed_form, 'error':error, 'urls':urls, 'sections':sections})


@login_required
def feed_view(request, feed_id=None):
    page = request.GET.get('page')

    feeder = get_feed(feed_id)
    paginator = Paginator(feeder.items.all(), 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'feed/feed_view.html', {'feed':feeder, 'news':news})


@login_required
def feed_list(request):
    sections = get_sections_by_user(request.user.id)
    return render(request, 'feed/feed_list.html', {'sections':sections})

@login_required
def feed_delete(request, section_id, feed_id):
    if user_has_feed(request.user.id, feed_id):
        section = get_section(section_id)
        section.feeds.remove(get_feed(feed_id))
        section.save()

    return redirect('feed_list')