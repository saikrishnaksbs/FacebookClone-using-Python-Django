from django.contrib import admin

from .models import Profile, Post, Comment, LikePost, Friend_Request, Friends, Chat

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Comment)
admin.site.register(Friend_Request)
admin.site.register(Friends)
admin.site.register(Chat)