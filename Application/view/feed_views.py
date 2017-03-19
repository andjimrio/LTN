from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect

from Application.forms import FeedForm
from Application.models import UserProfile,Feed
from Application.utilities.populate_utilities import populate_rss
from Application.utilities.queries_utilities import get_feeds_by_user,get_feed

@login_required
def feed_create(request):
    error = False

    if request.method == 'POST':
        feed_form = FeedForm(request.POST)

        if feed_form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            url = feed_form.data['url']
            try:
                ide = populate_rss(url)
                profile.feeds.add(Feed.objects.get(id=ide))
                redirect('feed_list')
            except:
                error = True

        else:
            print(feed_form.errors)

    else:
        feed_form = FeedForm()

    return render(request, 'feed/feed_create.html',{'feed_form':feed_form, 'error':error})


@login_required
def feed_view(request, idFeed=None):
    page = request.GET.get('page')

    feeder = get_feed(idFeed)
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
    feeds = get_feeds_by_user(request.user.id)
    return render(request, 'feed/feed_list.html', {'feeds':feeds})