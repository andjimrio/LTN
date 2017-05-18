from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Application.service.profile_services import get_profile, get_status_read_stats_by_user,\
    get_status_like_stats_by_user


@login_required
def profile_view(request):
    profile = get_profile(request.user.id)
    read_stats = get_status_read_stats_by_user(profile.id)
    like_stats = get_status_like_stats_by_user(profile.id)
    return render(request, 'profile/profile_view.html', {'profile': profile, 'read_stats': read_stats,
                                                         'like_stats': like_stats})
