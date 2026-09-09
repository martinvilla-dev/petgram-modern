"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views as auth
from post import views as post
from user_profile import views as profile
from notification import views as notify

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', auth.SignUpView.as_view(), name='signup'),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('404/', profile.error_404_view, name='404'),
    path('500/', profile.error_500_view, name='500'),
    path('follow/<int:user_id>/', profile.follow_view, name='follow'),
    path('unfollow/<int:user_id>/', profile.unfollow_view, name='unfollow'),
    path('edit/<int:user_id>/', profile.edit_profile_view, name='edit profile'),
    path('profile/<int:user_id>/', profile.profile_view, name='profile'),
    path('', post.homepage, name='homepage'),
    path('submit_post/', post.post_view, name='post_view'),
    path('post_detail/<int:post_id>/', post.post_detail, name='post_detail'),
    path('like/<int:post_id>/', post.like_view, name="like"),
    path('unlike/<int:post_id>/', post.unlike_view, name="unlike"),
    path('delete/<int:post_id>/', post.delete_post_view, name="delete"),
    path('comment_delete/<int:id>/', post.comment_delete, name='delete'),
    path('search/', profile.search_bar, name='search_bar'),
    path('notifications/', notify.notification_view, name='notification_view'),
    path('feed/', post.users_feed, name='user_feed'),
    path('hashtag/<slug:slug_id>/', post.hashtag_view, name='hashtag_view'),
    path('edit_post/<int:post_id>/', post.editPost_view, name='editpost'),
    path('deactivate/<int:user_id>/', profile.delete_user, name="delete_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

auth_handler404 = 'authentication.views.error_404_view'
notify_handler404 = 'notification.views.error_404_view'
post_handler404 = 'post.views.error_404_view'
user_handler404 = 'user_profile.views.error_404_view'
auth_handler500 = 'authentication.views.error_500_view'
notify_handler500 = 'notification.views.error_500_view'
post_handler500 = 'post.views.error_500_view'
user_handler500 = 'user_profile.views.error_500_view'