#encoding:utf-8
# Create your view here.
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

from Application.forms import UserForm
from Application.models import UserProfile,Feed


def home(request):
    return render(request,'index.html',{})

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = UserProfile()
            profile.user = user
            profile.save()

            return redirect('feed_list')

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'register.html',{'user_form':user_form})
