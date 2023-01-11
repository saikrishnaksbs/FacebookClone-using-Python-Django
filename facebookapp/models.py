from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, unique=True, error_messages={
        'unique': 'This field must be unique.'
    })
    ids = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to='profile_images', default='profile_images/blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    no_of_friends = models.IntegerField(default=0)
    no_of_followers = models.IntegerField(default=0)
    verified = models.IntegerField(default=0)
    friendnames = models.ManyToManyField(
        User, related_name='friendinlist', blank=True)
    following = models.ManyToManyField(
        User, related_name='followinglist', blank=True)
    followedby = models.ManyToManyField(
        User, related_name='followerslist', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)

    image = models.ImageField(upload_to='image_posts', blank=True)
    caption = models.TextField(blank=True)
    created_ad = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, related_name='likes', blank=True)
    postedby = models.ForeignKey(
        Profile, related_name='postedby', on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    likedusers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likedby')

    def __str__(self):
        return self.username


class Friends(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='friends', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    friends = models.CharField(max_length=100, blank=True)


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.to_user.username


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(default=datetime.now)
    commentedby = models.ForeignKey(
        Profile, related_name='commentedby', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Chat(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="receiver"
    )
    sendersname = models.CharField(max_length=40, blank=True)
    receiversname = models.CharField(max_length=40, blank=True)
    message = models.TextField(max_length=400)
    created = models.DateTimeField(default=datetime.now)
