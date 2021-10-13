from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    )

from blog.models import Post
from courses.models import CourseInfo, Course, ScheduleItem, Trainer
from datetime import datetime
import math

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect( 'userpage', username)
    else:
        form = UserRegisterForm()



    return render(request, 'users/register.html', {'form' : form})


@login_required
def profile(request):



    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account Updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form
        }


    return render(request, 'users/profile.html', context)


def userlist(request):
    context = {
        'users' : User.objects.all()
    }

    return render(request, f'users/user_list.html' ,context)


@login_required
def userpage(request, username):


    fuser = User.objects.get(username=username)

    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = fuser)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = fuser.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account Updated!')
            return redirect('userlist')
    else:
        user_form = UserUpdateForm(instance = fuser)
        profile_form = ProfileUpdateForm(instance = fuser.profile)

    context = {
        'fuser' : fuser,
        'user_form' : user_form,
        'profile_form' : profile_form
        }

    return render(request, 'users/userpage.html' , context)


@login_required
def useroptions(request, username):
    trainerItems = Trainer.objects.all()
    fuser = User.objects.get(username=username)


    x = []
    strained = 0
    days = 30

    for item in trainerItems:
        if fuser == item.user:
            dateItemStart = datetime.strptime(item.schedule.start.strftime("%Y/%m/%d"), "%Y/%m/%d" )
            dateItemEnd = datetime.strptime(item.schedule.end.strftime("%Y/%m/%d"), "%Y/%m/%d" )
            x.append(abs((dateItemStart - dateItemEnd).days))

    for element in x:
        strained += (2/math.pi)*math.atan(element/days)


    strained = round(strained, 2)

    context = {
        'fuser' : fuser,
        #'username' : fuser.username,
        'traineritems': trainerItems,
        'strain' : strained
    }

    return render(request, 'courses/userschedule.html', context)
