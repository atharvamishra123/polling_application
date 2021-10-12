from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render

from user.decorators import is_logged_in, is_registered, is_logout
from user.forms import UserCreationForm
from django.http import HttpResponseRedirect
from polls.forms import PollForm
from user.models import CustomUser


@is_registered
def user_registration(request):
    if request.method == "POST":
        fm = UserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/login/')
    else:
        fm = UserCreationForm()
    return render(request, 'signup.html', {'form': fm})


def show_profile(request):
    if request.method == 'GET':
        id = request.user.id
        user = CustomUser.objects.get(id=id)
        return render(request, "myprofile.html", {'data': user})


def user_profile(request, pk):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=pk)
        return render(request, "user_profile.html", {'data': user})


@is_logged_in
def user_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/allpolls/')
    else:
        fm = AuthenticationForm()
    return render(request, "login.html", {'form': fm})


def search_user_view(request):
    if request.method == "GET":
        query = request.GET.get("search")
        users = request.user.get_all_followings().values_list("id")
        user_id = [id[0] for id in users]
        users = CustomUser.objects.filter(Q(username__icontains=query) | Q(name__icontains=query))\
            .exclude(Q(id=request.user.id) | Q(id__in=user_id))
        return render(request, "user_list.html", {'users': users, 'is_follow': False})


def user_follow_view(request, id):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=id)
        current_user = request.user
        current_user.create_relationship(user)
        users = CustomUser.objects.filter(Q(username__icontains=user.username) | Q(name__icontains=user.name))\
            .exclude(Q(id=id) | Q(id=current_user.id))
        return render(request, "user_list.html", {'users': users, 'is_follow': False})


def user_unfollow_view(request, id):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=id)
        current_user = request.user
        current_user.remove_relationship(user)
        all_followings = current_user.get_all_followings()
        return render(request, "user_list.html", {'users': all_followings, 'is_follow': True})


def see_all_followings(request):
    if request.method == 'GET':
        current_user = CustomUser.objects.get(id=request.user.id)
        all_followings = current_user.get_all_followings()
        return render(request, "user_list.html", {'users': all_followings, 'is_follow': True})


def add_polls(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            instance = poll_form.save()
            instance.user = request.user
            instance.save()
            return render(request, "addpolls.html", {'form': poll_form})
    else:
        poll_form = PollForm()
    return render(request, "addpolls.html", {'form': poll_form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")
