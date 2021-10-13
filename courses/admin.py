from django.contrib import admin
from .models import CourseInfo, Course, Trainer, ScheduleItem

admin.site.register(CourseInfo)
admin.site.register(Course)
admin.site.register(ScheduleItem)
admin.site.register(Trainer)
# Register your models here.
