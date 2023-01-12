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
from .models import Profile, Post, Comment, LikePost, Friend_Request, Friends, Chat
from django.contrib.auth.decorators import login_required
from django.db import transaction
import datetime


def home(request):
    '''Directs to first page of website'''

    return render(request, 'home.html')


def signup(request):
    '''Directs to signup page'''

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
                return redirect('signup')
            else:
                user = User.objects.create_user(username=Username, password=Password,
                                                email=Email_Address, first_name=First_name, last_name=Last_name)
                user.save()
                user_model = User.objects.get(username=Username)
                new_profile = Profile.objects.create(
                    user=user_model, ids=user_model.id)
                new_profile.save()
                return redirect('login')

        else:
            messages.info(request, 'Should enter same password')
            return redirect('')

    else:
        return render(request, 'signup.html')


def login(request):
    '''Directs to login page'''

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
    '''Directs to login page'''
    auth.logout(request)
    return redirect('login')


@login_required
@transaction.atomic
def settings(request):
    '''Directs to settings page where you can change profilepic,bio,location'''
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


@login_required
@transaction.atomic
def coverpic(request):
    '''Gets the coverpic data'''
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.coverimg
            user_profile.coverimg = image
            user_profile.save()

        if request.FILES.get('image') != None:

            image = request.FILES.get('image')
            user_profile.coverimg = image
            user_profile.save()

        return redirect('profile')
    return render(request, 'coverpic.html')


@login_required
@transaction.atomic
def profile(request):
    '''Directs to profile page of user'''
    username = User.objects.get(username=request.user.username)
    usercheck = Profile.objects.all().filter(ids=request.user.id)
    friend_list = list(Friends.objects.filter(name=username).values('friends'))
    allfriends = []
    likeposts = list(LikePost.objects.filter(likedusers=username))
    for friend in friend_list:
        allfriends.append(friend['friends'])
    profileimages = Profile.objects.filter(user__username__in=allfriends)

    if usercheck.count() == 0:
        alldetails = {'name': username,
                      'userprofile': None,
                      }
        return render(request, 'newprofile.html', {'output': alldetails, 'friend_list': friend_list, 'profileimages': profileimages})
    else:
        userprofile = Profile.objects.get(user=username)
        postscheck = Post.objects.all().filter(user=username)

        if postscheck.count() == 0:
            alldetails = {'name': username,
                          'userprofile': userprofile,
                          }
            return render(request, 'newprofile.html', {'output': alldetails, 'friend_list': friend_list, 'profileimages': profileimages})

        else:
            posts = Post.objects.filter(
                user=userprofile).order_by('-created_ad')
            alldetails = {'name': request.user.username,
                          'userprofile': userprofile,
                          }
            return render(request, 'newprofile.html', {'output': alldetails, 'posts': posts, 'friend_list': friend_list, 'profileimages': profileimages, 'liked_details': likeposts})


@login_required
@transaction.atomic
def postuploading(request):
    '''Directs to status upload page'''
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST['caption']
        profile_of_postedperson = Profile.objects.get(ids=request.user.id)
        if not image:
            new_post = Post.objects.create(
                user=user, caption=caption, postedby=profile_of_postedperson)
            new_post.save()
            return redirect('profile')
        else:
            new_post = Post.objects.create(postedby=profile_of_postedperson,
                                           user=user, image=image, caption=caption)
            new_post.save()
            return redirect('profile')

    else:
        return render(request, 'post.html')


@login_required
@transaction.atomic
def postdeletion(request, id):
    '''Deletes the post'''
    blogpost = Post.objects.get(id=id)
    blogpost.delete()
    return redirect('profile')


@login_required
@transaction.atomic
def search(request):
    '''Directs to searched page'''

    searched_name = request.GET
    searched_details = searched_name.get("name")
    requested_userid = request.user.id
    searched_name = User.objects.filter(username=searched_details)
    Friend_list = list(Friends.objects.filter(
        name=searched_details).values('friends'))

    allfriends = []
    for friend in Friend_list:
        allfriends.append(friend['friends'])
    profileimages = Profile.objects.filter(user__username__in=allfriends)
    print(profileimages)

    requesteduserprofile = Profile.objects.filter(ids=requested_userid)
    print(requesteduserprofile)

    if searched_name.count() == 0:
        return HttpResponse(searched_details+" does not exist")
    else:
        username = User.objects.get(username=searched_details)
        print(username, username.id)
        usercheck = Profile.objects.all().filter(ids=username.id)
        if usercheck.count() == 0:
            alldetails = {'name': searched_details,
                          'userprofile': None,
                          'searchedby': requested_userid,
                          }
            return render(request, 'viewprofile.html', {'output': alldetails, 'profileimages': profileimages})
        else:
            userprofile = Profile.objects.get(user=username)
            postscheck = Post.objects.all().filter(user=username)

            if postscheck.count() == 0:
                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              'searchedby': requested_userid,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails, 'profileimages': profileimages})

            else:
                posts = Post.objects.filter(
                    user=searched_details).order_by('-created_ad')

                alldetails = {'name': searched_details,
                              'userprofile': userprofile,
                              'searchedby': requested_userid,
                              }
                return render(request, 'viewprofile.html', {'output': alldetails, 'posts': posts, 'profileimages': profileimages})


@login_required
@transaction.atomic
def like_post(request):
    '''Directs to like page'''

    if request.method == 'POST':

        postid = request.POST.get('post_id')
        profileid = request.POST.get('profile_id')
        username = request.user.username
        post = Post.objects.get(id=postid)

        likedusers = User.objects.get(id=request.user.id)
        like_filter = LikePost.objects.filter(
            post_id=postid, username=username).exists()
        like_filter_data = LikePost.objects.filter(
            post_id=postid, username=username)

        if not like_filter:
            print("added like")
            new_like = LikePost.objects.create(
                post_id=postid, username=username, likedusers=likedusers)
            new_like.save()
            post.liked.add(request.user)
            post.no_of_likes = post.no_of_likes+1
            post.save()
            color = 'blue'
            return JsonResponse({'likes': post.no_of_likes, 'post_id': postid, 'color': color})
        else:
            print("deleted like")
            like_filter_data.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
            post.liked.remove(request.user)
            post.save()
            color = 'white'
            return JsonResponse({'likes': post.no_of_likes, 'post_id': postid, 'color': color})


@login_required
@transaction.atomic
def postComment(request):
    '''Here you can post your comments'''

    if request.method == "POST":

        id = request.POST.get('postid')
        comment = request.POST.get('comment')
        post = Post.objects.get(id=id)
        name = request.user.username
        profileimg = request.user.profile.profileimg.url
        profile_of_commenter = Profile.objects.get(ids=request.user.id)
        body = comment
        print(body, comment, id)
        comments = Comment.objects.create(
            post=post, commentedby=profile_of_commenter, name=name, body=body)
        name = request.user.username
        body = comment
        comments.save()
        return JsonResponse({'comment': body, 'name': name, 'profileimg': profileimg, })


@login_required
@transaction.atomic
def addrequest(request):
    '''Here you can send friend request'''

    if request.method == 'POST':

        searchedbyid = request.POST.get('searchedbyid')
        searchedid = request.POST.get('searchedid')
        searchedname = request.POST.get('searchedname')

        searchedbyid_object = User.objects.get(id=searchedbyid)
        searchedid_object = User.objects.get(id=searchedid)
        checking_friendrequest = Friends.objects.filter(
            name=searchedname, friends=request.user.username).exists()

        print(checking_friendrequest)
        if checking_friendrequest:
            response = "already friends"
            return JsonResponse({'response': response})

        if not Friend_Request.objects.filter(from_user=searchedbyid_object, to_user=searchedid_object).exists():

            friendrequest = Friend_Request.objects.create(
                from_user=searchedbyid_object, to_user=searchedid_object)
            friendrequest.save()
            response = "sent"
            return JsonResponse({'response': response})
        else:
            response = "Request already sent"
            return JsonResponse({'response': response})


@login_required
@transaction.atomic
def friendrequests(request):
    '''Here you can collect friendrequests list'''

    userid = request.user.id
    friendrequests = Friend_Request.objects.filter(to_user__id=userid)
    print(friendrequests)
    return render(request, 'friendlist.html', {'friendslist': friendrequests})


@login_required
@transaction.atomic
def acceptrequest(request):
    '''Here you can accept the requests'''

    if request.method == 'POST':
        friendid = request.POST.get('friendid')
        friendname = request.POST.get('friendname')

        print(friendid, friendname)

        sender_friend_object = Profile.objects.get(ids=friendid)
        accepted_friend_object = Profile.objects.get(ids=request.user.id)

        print(sender_friend_object, accepted_friend_object)

        if not Friends.objects.filter(profile=sender_friend_object, friends=request.user.username).exists():
            sender_friend = Friends.objects.create(
                profile=sender_friend_object, name=friendname, friends=request.user.username)
            accepted_friend = Friends.objects.create(
                profile=accepted_friend_object, name=request.user.username, friends=friendname)

            sender_friend.save()
            accepted_friend.save()

            friendrequests = Friend_Request.objects.filter(
                to_user__id=request.user.id, from_user__id=friendid)
            friendrequests.delete()

            senduser = User.objects.get(id=friendid)
            sender_friend_object.friendnames.add(request.user)
            accepted_friend_object.friendnames.add(senduser)
            sender_friend_object.no_of_friends = sender_friend_object.no_of_friends+1
            accepted_friend_object.no_of_friends = accepted_friend_object.no_of_friends+1

            sender_friend_object.save()
            accepted_friend_object.save()

            message = "You are friends now"
            return JsonResponse({'message': message})
        else:
            message = "You are friends already"
            return JsonResponse({'message': message})


@login_required
@transaction.atomic
def rejectrequest(request):
    '''Here you can reject friends'''

    if request.method == 'POST':

        friendid = request.POST.get('friendid')
        friendname = request.POST.get('friendname')
        friendrequests = Friend_Request.objects.filter(
            to_user__id=request.user.id, from_user__id=friendid)
        friendrequests.delete()
        message = "Request Deleted"
        return JsonResponse({'message': message})


@login_required
@transaction.atomic
def friendslist(request, id):
    '''Displays friends list'''

    print(id)
    profile_details = Profile.objects.get(ids=id)
    Friend_list = Friends.objects.filter(profile=profile_details)
    return render(request, 'allfriendslist.html', {'Friend_list': Friend_list})


@login_required
@transaction.atomic
def allfriendslist(request, id):
    '''Displays all friends of a searched person'''

    print(id)
    profile_details = Profile.objects.get(ids=id)
    Friend_list = Friends.objects.filter(profile=profile_details)
    return render(request, 'allviewfriendslist.html', {'Friend_list': Friend_list})


@login_required
@transaction.atomic
def removefriend(request):
    '''Here i can remove my friend'''

    if request.method == 'POST':

        friendname = request.POST.get('friendname')
        friendid = request.POST.get('friendid')
        adminname = request.user.username
        adminid = request.user.id
        print(friendid, friendname, adminname, adminid)

        adminobject = Profile.objects.get(user__username=adminname)
        friendobjeject = Profile.objects.get(user__username=friendname)
        print(friendobjeject, adminobject)

        adminlist = Friends.objects.filter(name=friendname, friends=adminname)
        friendlist = Friends.objects.filter(name=adminname, friends=friendname)
        print(adminlist, friendlist)

        print(friendid, friendname)
        senduser = User.objects.get(username=friendname)
        friendobjeject.friendnames.remove(request.user)
        adminobject.friendnames.remove(senduser)

        friendobjeject.no_of_friends = friendobjeject.no_of_friends-1
        adminobject.no_of_friends = adminobject.no_of_friends-1

        friendobjeject.save()
        adminobject.save()
        adminlist.delete()
        friendlist.delete()

        message = "Friend Deleted"
        return JsonResponse({'message': message})


@login_required
@transaction.atomic
def messagelist(request, id):
    '''Here you can fine whom you can message'''

    profile_details = Profile.objects.get(ids=request.user.id)
    Friend_list = Friends.objects.filter(profile=profile_details)
    return render(request, 'messageslist.html', {'Friend_list': Friend_list})


@login_required
@transaction.atomic
def sendmessage(request, friends):
    '''Here you can create a message'''

    profile_details = Profile.objects.get(user__username=friends)
    messagedetails = Friends.objects.filter(profile=profile_details)
    return render(request, 'message.html', {'messagedetails': messagedetails, 'friendname': friends})


@login_required
@transaction.atomic
def tomessage(request):
    '''Here you can send the message'''

    if request.method == "POST":
        print("in tomessages")
        sender = request.user.username
        receiver = request.POST.get('friendsname')
        message = request.POST.get("message")
        print(sender, receiver, message)
        senderprofile = Profile.objects.get(user__username=sender)
        receiverprofile = Profile.objects.get(user__username=receiver)
        print(senderprofile, receiverprofile)

        createchat = Chat.objects.create(sender=senderprofile,
                                         receiver=receiverprofile,
                                         sendersname=sender,
                                         receiversname=receiver,
                                         message=message,
                                         )
        createchat.save()
        print("chat created")
        message = "Message saved"
        return JsonResponse({'message': message})


@login_required
@transaction.atomic
def getmessage(request, friendname):
    '''Here you can view the messages'''

    if request.method == "GET":
        sender = Profile.objects.get(ids=request.user.id)
        receiver = Profile.objects.get(user__username=friendname)

        allmessages = Chat.objects.filter(
            Q(sender=sender, receiver=receiver)
            | Q(sender=receiver, receiver=sender)
        )
        chats = list(allmessages.values())
        return JsonResponse({'chats': chats})


def postfeed(request):
    username = User.objects.get(username=request.user.username)
    usercheck = Profile.objects.all().filter(ids=request.user.id)
    friend_list = list(Friends.objects.filter(name=username).values('friends'))
    allfriends = []
    likeposts = list(LikePost.objects.filter(likedusers=username))
    for friend in friend_list:
        allfriends.append(friend['friends'])
    profileimages = Profile.objects.filter(user__username__in=allfriends)

    print(allfriends)
    friendsposts = Post.objects.filter(
        user__in=allfriends).order_by('-created_ad')
    print(friendsposts)

    userprofile = Profile.objects.get(user=username)
    alldetails = {'name': username,
                  'userprofile': userprofile,
                  }
    return render(request, 'postfeed.html', {'output': alldetails, 'allposts': friendsposts})


def follow(request):
    if request.method == 'POST':

        searchedbyid = request.POST.get('searchedbyid')
        searchedid = request.POST.get('searchedid')
        searchedname = request.POST.get('searchedname')

        searchedbyid_object = Profile.objects.get(ids=searchedbyid)
        searchedid_object = Profile.objects.get(ids=searchedid)

        searchedbyid_user_object = User.objects.get(id=searchedbyid)
        searchedid_user_object = User.objects.get(id=searchedid)

        if searchedbyid_user_object not in searchedid_object.followedby.all():
            print("not in ------ follow")
            searchedbyid_object.following.add(searchedid_user_object)
            searchedid_object.followedby.add(searchedbyid_user_object)
            searchedid_object.no_of_followers = searchedid_object.no_of_followers+1
            searchedid_object.save()
            searchedid_object.save()
            followers_count = searchedid_object.no_of_followers
            return JsonResponse({'followers_count': followers_count, 'msg': 'Unfollow'})

        else:
            print("yes it is in ---------follow")
            followers_count = searchedid_object.no_of_followers
            return JsonResponse({'followers_count': followers_count, 'msg': 'Unfollow'})


def unfollow(request):

    if request.method == 'POST':

        searchedbyid = request.POST.get('searchedbyid')
        searchedid = request.POST.get('searchedid')
        searchedname = request.POST.get('searchedname')

        searchedbyid_object = Profile.objects.get(ids=searchedbyid)
        searchedid_object = Profile.objects.get(ids=searchedid)

        searchedbyid_user_object = User.objects.get(id=searchedbyid)
        searchedid_user_object = User.objects.get(id=searchedid)

        if searchedbyid_user_object in searchedid_object.followedby.all():
            print("not in ----------unfollow")
            searchedbyid_object.following.remove(searchedid_user_object)
            searchedid_object.followedby.remove(searchedbyid_user_object)
            searchedid_object.no_of_followers = searchedid_object.no_of_followers-1

            searchedid_object.save()
            searchedid_object.save()
            followers_count = searchedid_object.no_of_followers
            return JsonResponse({'followers_count': followers_count, 'msg': 'Follow'})

        else:
            print("yes it is in ------unfollow")
            followers_count = searchedid_object.no_of_followers
            return JsonResponse({'followers_count': followers_count, 'msg': 'Follow'})
