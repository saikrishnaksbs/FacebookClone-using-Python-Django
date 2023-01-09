from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('profile', views.profile, name='profile'),
    path('postuploading', views.postuploading, name='postuploading'),
    path('postdeletion/<uuid:id>', views.postdeletion, name='postdeletion'),
    path('search', views.search, name='search'),
    path('like-post', views.like_post, name='like-post'),
    path('addrequest', views.addrequest, name='addrequest'),
    path('postComment', views.postComment, name='postComment'),
    path('friendrequests', views.friendrequests, name='friendrequests'),
    path('acceptrequest', views.acceptrequest, name='acceptrequest'),
    path('rejectrequest', views.rejectrequest, name='rejectrequest'),
    path('friendslist/<int:id>', views.friendslist, name='friendslist'),
    path('removefriend', views.removefriend, name='removefriend'),
    path('messagelist/<int:id>', views.messagelist, name='messagelist'),
    path('sendmessage/<str:friends>', views.sendmessage, name='sendmessage'),
    path('tomessage', views.tomessage, name='tomessage'),
    path('getmessage/<str:friendname>', views.getmessage, name='getmessage'),
    path('allfriendslist/<int:id>', views.allfriendslist, name='allfriendslist'),
    path('postfeed', views.postfeed, name='postfeed'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
]
