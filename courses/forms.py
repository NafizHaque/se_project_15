from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ScheduleItem, Trainer, Course, CourseInfo





class ScheduleItemForm(forms.ModelForm):
    class Meta:
        model = ScheduleItem
        fields = ['start','end', 'course']



class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['user']