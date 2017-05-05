from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Application.utilities.queries_utilities import get_profile

@login_required
def profile_view(request):
    profile = get_profile(request.user.id)
    return render(request, 'profile/profile_view.html', {'profile': profile})