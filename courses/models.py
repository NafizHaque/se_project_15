from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class CourseInfo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses-detail', kwargs ={'pk':self.pk})

class Course(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    course_info = models.ForeignKey(CourseInfo, on_delete = models.CASCADE)

    def __str__(self):
        return self.start_date.strftime("%Y/%m/%d") + " - " + self.end_date.strftime("%Y/%m/%d") + " : " + str(self.course_info)


    def get_absolute_url(self):
        return reverse('courseobject-detail', kwargs ={'pk':self.pk})

class ScheduleItem(models.Model):
    start = models.DateField()
    end = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.start.strftime("%Y/%m/%d") + "  to  " + self.end.strftime("%Y/%m/%d") + " : " + str(self.course.course_info.title)

class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    schedule = models.ForeignKey(ScheduleItem, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.user) + " - " + str(self.schedule.start.strftime("%Y/%m/%d"))
