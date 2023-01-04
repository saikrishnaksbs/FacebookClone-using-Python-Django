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
from .models import Profile, Post, Comment, LikePost
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
    print(searched_details, searched_name)

    searched_name = User.objects.filter(username=searched_details)
    print(searched_name)
    if searched_name.count() == 0:
        return HttpResponse(searched_details+" does not exist")
    else:
        username = User.objects.get(username=searched_details)

        print(username, username.id)
        usercheck = Profile.objects.all().filter(id_user=username.id)
        if usercheck.count() == 0:
            alldetails = {'name': searched_details,
                          'userprofile': None,
                          }
            return render(request, 'viewprofile.html', {'output': alldetails})
        else:
            userprofile = Profile.objects.get(user=username)
            postscheck = Post.objects.all().filter(user=username)

            if postscheck.count() == 0:
                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails})

            else:
                posts = Post.objects.filter(user=searched_details)
                
                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails, 'posts': posts})


def like_post(request):
    if request.method == 'POST':
        postid = request.POST.get('post_id')
        profileid = request.POST.get('profile_id')
        
        username = request.user.username
        post = Post.objects.get(id=postid)
        print(post,username,profileid,postid)
        like_filter = LikePost.objects.filter(
            post_id=postid, username=username).exists()
        print(like_filter)
        
        like_filter_data = LikePost.objects.filter(post_id=postid, username=username)
        print(like_filter_data)
        print("--------")
        
        if not like_filter:
            new_like = LikePost.objects.create(
                post_id=postid, username=username)
            new_like.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()
         
            return JsonResponse({'likes': post.no_of_likes,'post_id':postid})

        else:
            like_filter_data.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
          
            return JsonResponse({'likes': post.no_of_likes,'post_id':postid})


def postComment(request,id):
    
    if request.method == "POST":
        
        blogpost = Post.objects.get(id=id)
        comment=request.POST.get('comment')
        post = Post.objects.get(id=id)
        name=request.user.username
        body=comment
        comments=Comment.objects.create(post=post,name=name,body=body)
        comments.save()
                
        return redirect('profile')
       

# def send_friend_request(request,userID):
#     from_user=request.user
#     to_user=User.objects.gegt(id=userID)
#     friend_request=Friend_Request.objects.get_or_create(from_user=from_user,to_user=to_user,status='pending')
    
# def accept_friend_request(request,requsestID):
#     friend_request=Friend_Request.objects.get(id=requsestID)
#     if friend_request.to_user==request.user:
#         friend_request.to_user.friends.add(friend_request.from_user)
#         friend_request.from_user.friends.add(friend_request.to_user)
#         friend_request.delete()
#         return HttpResponse('friend request accepted')
#     else:
#         return HttpResponse('friend request not accepted')