from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from social_django.models import UserSocialAuth
import json
from .models import PostData,LoginUser
import ast

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj=LoginUser.objects.filter(username=username,password=password).count()
        if obj > 0:
            print('okk')
            return redirect('https://growthplug-facebook-app.herokuapp.com/')
        else:
            return redirect('/')

def post_data(request):
    data    = request.body
    convert =data.decode("utf-8")
    lst=convert.split(',')
    if len(lst) == 2:
        title=lst[0]
        desc=lst[1]
        obj=PostData.objects.create(title=lst[0],desc=lst[1])
    return JsonResponse({"code":200})

def display_users(request):
    data=list(PostData.objects.values())
    return JsonResponse(data,safe=False)

def update_data(request,id):
    print(id)
    data    = request.body
    convert =data.decode("utf-8")
    lst=convert.split(',')
    obj=PostData.objects.filter(pk=id).update(title=lst[0],desc=lst[1])
    return JsonResponse({"code":200})

def delete_data(request,id):
    print(id)
    data=PostData.objects.filter(pk=id).delete()
    return JsonResponse({"code":200})


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
