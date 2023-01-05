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
from .models import Profile, Post, Comment, LikePost, Friend_Request, Friends
from django.contrib.auth.decorators import login_required
from django.db import transaction
import datetime


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
                user_model = User.objects.get(username=Username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
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
            return redirect('profile')

        else:
            messages.info(request, 'Check Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


@login_required
@transaction.atomic
def logout(request):
    auth.logout(request)
    return redirect('/')


def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

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

        return redirect('profile')
    return render(request, 'settings.html')


def profile(request):
    username = User.objects.get(username=request.user.username)
    print(username)
    usercheck = Profile.objects.all().filter(id_user=request.user.id)
    if usercheck.count() == 0:
        alldetails = {'name': username,
                      'userprofile': None,
                      }
        return render(request, 'newprofile.html', {'output': alldetails})
    else:
        userprofile = Profile.objects.get(user=username)
        postscheck = Post.objects.all().filter(user=username)

        if postscheck.count() == 0:
            alldetails = {'name': username,
                          'userprofile': userprofile,
                          }
            return render(request, 'newprofile.html', {'output': alldetails})

        else:
            posts = Post.objects.filter(user=userprofile)
            alldetails = {'name': request.user.username,
                          'userprofile': userprofile,
                          }
            return render(request, 'newprofile.html', {'output': alldetails, 'posts': posts})


def postuploading(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('profile')

    else:
        return render(request, 'post.html')


def postdeletion(request, id):
    blogpost = Post.objects.get(id=id)
    blogpost.delete()
    return redirect('profile')


def search(request):
    searched_name = request.GET
    searched_details = searched_name.get("name")
    requested_userid = request.user.id
    searched_name = User.objects.filter(username=searched_details)
    print(searched_name, requested_userid)
    if searched_name.count() == 0:
        return HttpResponse(searched_details+" does not exist")
    else:
        username = User.objects.get(username=searched_details)

        print(username, username.id)
        usercheck = Profile.objects.all().filter(id_user=username.id)
        if usercheck.count() == 0:
            alldetails = {'name': searched_details,
                          'userprofile': None,
                          'searchedby': requested_userid,
                          }
            return render(request, 'viewprofile.html', {'output': alldetails})
        else:
            userprofile = Profile.objects.get(user=username)
            postscheck = Post.objects.all().filter(user=username)

            if postscheck.count() == 0:
                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              'searchedby': requested_userid,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails})

            else:
                posts = Post.objects.filter(user=searched_details)

                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              'searchedby': requested_userid,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails, 'posts': posts})


def like_post(request):
    if request.method == 'POST':
        postid = request.POST.get('post_id')
        profileid = request.POST.get('profile_id')

        username = request.user.username
        post = Post.objects.get(id=postid)
        print(post, username, profileid, postid)
        like_filter = LikePost.objects.filter(
            post_id=postid, username=username).exists()
        print(like_filter)

        like_filter_data = LikePost.objects.filter(
            post_id=postid, username=username)
        print(like_filter_data)
        print("--------")

        if not like_filter:
            new_like = LikePost.objects.create(
                post_id=postid, username=username)
            new_like.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()

            return JsonResponse({'likes': post.no_of_likes, 'post_id': postid})

        else:
            like_filter_data.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()

            return JsonResponse({'likes': post.no_of_likes, 'post_id': postid})


def postComment(request, id):

    if request.method == "POST":

        blogpost = Post.objects.get(id=id)
        comment = request.POST.get('comment')
        post = Post.objects.get(id=id)
        name = request.user.username
        body = comment
        comments = Comment.objects.create(post=post, name=name, body=body)
        comments.save()

        return redirect('profile')


def addrequest(request):
    if request.method == 'POST':
        searchedbyid = request.POST.get('searchedbyid')
        searchedid = request.POST.get('searchedid')

        searchedbyid_object = User.objects.get(id=searchedbyid)
        searchedid_object = User.objects.get(id=searchedid)
        if not Friend_Request.objects.filter(from_user=searchedbyid_object, to_user=searchedid_object).exists():

            friendrequest = Friend_Request.objects.create(
                from_user=searchedbyid_object, to_user=searchedid_object)
            friendrequest.save()
            response = "sent"
            return JsonResponse({'response': response})
        else:
            response = "Request already sent"
            return JsonResponse({'response': response})


def friendrequests(request):
    userid = request.user.id
    friendrequests = Friend_Request.objects.filter(to_user__id=userid)
    print(friendrequests)
    return render(request, 'friendlist.html', {'friendslist': friendrequests})


def acceptrequest(request):

    if request.method == 'POST':
        friendid = request.POST.get('friendid')
        friendname = request.POST.get('friendname')
        sender_friend_object = Profile.objects.get(id_user=friendid)
        accepted_friend_object = Profile.objects.get(id_user=request.user.id)

        print(friendid, request.user.id, sender_friend_object)
        if not Friends.objects.filter(profile=sender_friend_object, friends=request.user.username).exists():
            sender_friend = Friends.objects.create(
                profile=sender_friend_object, friends=request.user.username)
            accepted_friend = Friends.objects.create(
                profile=accepted_friend_object, friends=friendname)
            sender_friend.save()
            accepted_friend.save()
            friendrequests = Friend_Request.objects.filter(
                to_user__id=request.user.id, from_user__id=friendid)
            friendrequests.delete()
            message = "You are friends now"
            return JsonResponse({'message': message})


def rejectrequest(request):

    if request.method == 'POST':
        friendid = request.POST.get('friendid')
        friendname = request.POST.get('friendname')
        friendrequests = Friend_Request.objects.filter(
            to_user__id=request.user.id, from_user__id=friendid)
        friendrequests.delete()
        message = "Request Deleted"
        return JsonResponse({'message': message})


def friendslist(request, id):
    print(id)
    profile_details = Profile.objects.get(id_user=id)
    Friend_list = Friends.objects.filter(profile=profile_details)
    return render(request, 'allfriendslist.html', {'Friend_list': Friend_list})
