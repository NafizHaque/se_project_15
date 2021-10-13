from django.urls import path
from . import views
from .views import (
    CourseInfoListView,
    CourseInfoUpdateView,
    CourseInfoCreateView,
    CourseInfoDetailView,
    CourseInfoDeleteView,
    CourseObjectListView,
    CourseObjectCreateView,
    CourseObjectDetailView,
    CourseObjectUpdateView,
    CourseObjectDeleteView,

    Scheduleitem,
    CourseObjectsHome,
)

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('courseinfo/', CourseInfoListView.as_view(), name="courses-home"),
    path('courseinfo/new/', login_required(CourseInfoCreateView.as_view()), name="courses-create"),
    path('courseinfo/<int:pk>/', login_required(CourseInfoDetailView.as_view()) ,name = 'courses-detail'),
    path('courseinfo/<int:pk>/update', CourseInfoUpdateView.as_view(), name="courses-update"),
    path('courseinfo/<int:pk>/delete/', login_required(CourseInfoDeleteView.as_view()), name = 'courses-delete'),

    path('courseobject/', CourseObjectListView.as_view(), name="courseobject-home"),
    path('courseobject/<int:pk>/update', CourseObjectUpdateView.as_view(), name="courseobject-update"),
    path('courseobject/new/', CourseObjectCreateView.as_view(), name="courseobject-create"),
    path('courseobject/<int:pk>', CourseObjectDetailView.as_view(), name="courseobject-detail"),
    path('courseobject/<int:pk>/delete', CourseObjectDeleteView.as_view(), name="courseobject-update"),

    path('scheduleitem/new/', views.Scheduleitem ,name = 'scheduleitem-create'),
    path('courseobject/<str:username>', views.CourseObjectsHome, name="courseobject-home-schedule"),
    path(r'^scheduleitem/(?P<username>[\w\-]+)/$', views.ScheduleItemHome, name="scheduleitem"),

]
