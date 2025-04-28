"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from core import views as core_views
from django.contrib.auth import views as auth_views
from core import views as core_views
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
  path('accounts/', include([
        path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
        path('logout/', accounts_views.user_logout, name='logout'),
        path('register/', accounts_views.register, name='register'),
        path('profile/', accounts_views.profile, name='profile'),
        path('profile/edit/', accounts_views.profile_edit, name='profile_edit'),
        path('profile/change-password/', accounts_views.change_password, name='change_password'),
        path('profile/<str:username>/', accounts_views.profile, name='user_profile'),
    ])),
    # Profile
    path('profile/', accounts_views.profile, name='profile'),
    path('profile/edit/', accounts_views.profile_edit, name='profile_edit'),
    path('profile/change-password/', accounts_views.change_password, name='change_password'),
    path('profile/<str:username>/', accounts_views.profile, name='user_profile'),
    
    # Core
    path('', core_views.home, name='home'),
     path('post/create/', core_views.post_create, name='post_create'),
    path('post/delete/<int:post_id>/', core_views.delete_post, name='delete_post'),
 
   
    path('example/', core_views.example_view, name='example'),
   
    path('', core_views.home, name='home'),
    path('search/', core_views.search, name='search'),
    path('create-story/', core_views.create_story, name='create_story'),
 
    path('post/<int:post_id>/', core_views.post_detail, name='post_detail'),
    path('stories/', core_views.view_stories, name='view_stories'),
    path('stories/create/', core_views.create_story, name='create_story'),
    path('post/<int:post_id>/', core_views.post, name='post_detail'),
    path('post/<int:post_id>/comments/', core_views.comment_view, name='comment_view'),
     path('post/<int:post_id>/likes/', core_views.like_view, name='like_view'),

    
    
    path('post/<int:post_id>/edit/', core_views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', core_views.post_delete, name='post_delete'),
    # Friends

 
    path('friend/', core_views.friend_view, name='friend_page'),
    path('send-friend-request/<int:user_id>/', core_views.send_friend_request, name='send_friend_request'),
    path('manage-friend-requests/', core_views.manage_friend_requests, name='manage_friend_requests'),
    path('respond-friend-request/<int:request_id>/<str:action>/', core_views.respond_friend_request, name='respond_friend_request'),

    
    # Stories
    path('stories/', core_views.view_stories, name='view_stories'),
    path('stories/create/', core_views.create_story, name='create_story'),
    
    # Search
    path('search/', core_views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)