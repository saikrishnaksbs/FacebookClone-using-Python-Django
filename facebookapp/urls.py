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
    path('postComment/<uuid:id>', views.postComment, name='postComment')
]
