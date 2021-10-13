"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path
from .views import (PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    NotificationView,
    QualificationView,
    PostQualificationView,
    QualificationDetailView,
    QualificationDeleteView,
    HomeView,


    
    )
    
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(HomeView.as_view()) ,name = 'blog-home'),
    path('user/<str:username>', login_required(UserPostListView.as_view()) ,name = 'user-posts'),
    path('post/<int:pk>/', login_required(PostDetailView.as_view()) ,name = 'post-detail'),
    path('post/new/', login_required(PostCreateView.as_view()) ,name = 'post-create'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()) ,name = 'post-update'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()) ,name = 'post-delete'),
    path('about/', views.about ,name = 'blog-about'),
    path('links/', views.links ,name = 'links'),

    path('qualification/',  login_required(QualificationView.as_view()) ,name = 'qualifications'),
    path('notification/',  login_required(NotificationView.as_view()) ,name = 'notification'),
    path('qualification/new/', login_required(PostQualificationView.as_view()) ,name = 'post-qualifications'),
    path('qualification/<int:pk>/',  login_required(QualificationDetailView.as_view()) ,name = 'qualifications-detail'),
    path('qualification/<int:pk>/delete/', login_required(QualificationDeleteView.as_view()) ,name = 'qualifications-delete'),
    


]

