from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from Application.forms import UserForm,UserProfileForm
from Application.models import UserProfile,Feed
from Application.utilities.populate_utilities import populate_rss
from Application.utilities.queries_utilities import get_feeds_by_user,get_feed

@login_required
def feed_create(request):
    if request.method == 'POST':
        feed_form = UserProfileForm(request.POST)

        if feed_form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            for url in fee_form.data['urls'].split('\r\n'):
                ide = populate_rss(url)
                profile.feeds.add(Feed.objects.get(id=ide))

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
    return


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