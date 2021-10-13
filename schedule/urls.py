from django.urls import path

from . import views
from courses.views import ScheduleItemHome

urlpatterns = [
    path('', views.index, name='schedule'),
    path('download/', views.download, name='schedule-download'),
]
