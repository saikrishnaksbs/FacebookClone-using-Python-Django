from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.db import transaction
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count, F, Value, Q
from django.db import connection
from django.db.models import OuterRef, Subquery
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'POST':
        First_name = request.POST['first_name']
        Last_name = request.POST['last_name']
        Email_Address = request.POST['email']
        Password = request.POST['password']
        Username = request.POST['username']
        Confirm_Password = request.POST['confirm']

        if (Password == Confirm_Password):

            if User.objects.filter(username=Username).exists():
                messages.info(request, 'UserName already taken')
                return redirect('')
            elif User.objects.filter(email=Email_Address).exists():
                messages.info(request, 'Email already taken')
                return redirect('')
            else:
                user = User.objects.create_user(username=Username, password=Password,
                                                email=Email_Address, first_name=First_name, last_name=Last_name)
                user.save()
                return redirect('login')

        else:
            messages.info(request, 'Should enter same password')
            return redirect('')

    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        usernames = request.POST['username']
        passwords = request.POST['password']
        user = auth.authenticate(username=usernames, password=passwords)

        if user is not None:
            auth.login(request, user)
            print(user)
            return render(request, 'profile.html', {'output': user})

        else:
            messages.info(request, 'Check Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def settings(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:

            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('login')
    return render(request, 'settings.html')
