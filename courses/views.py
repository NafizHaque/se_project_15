from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from .models import CourseInfo, Course, ScheduleItem, Trainer
from .forms import ScheduleItemForm, TrainerForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
import math



def index(request):
    context = {
        'courses': CourseInfo.objects.all()
    }
    return render(request, 'courses/content.html', context)

class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'courses/content.html'
    context_object_name = 'courseinfos'
    # ordering = ['-date_posted']

class CourseInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CourseInfo
    template_name = 'courses/courseinfo-create.html'
    context_object_name = 'courseinfos'
    fields = ['title', 'description']

    def test_func(self):
        return True

    def form_valid(self, form):
        form.instance.recipient = self.request.user
        return super().form_valid(form)

class CourseInfoCreateView(LoginRequiredMixin, CreateView):
    model = CourseInfo
    fields = ['title', 'description']
    template_name = 'courses/courseinfo-create.html'
    context_object_name = 'courseinfos'

    def form_valid(self, form):
        return super().form_valid(form)

class CourseInfoDetailView(DetailView):
    model = CourseInfo

    def get_context_data(self, *args, **kwargs):
        context = super(CourseInfoDetailView, self).get_context_data(*args, **kwargs)
        context['courseobjects'] = Course.objects.all()
        return context

class CourseInfoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CourseInfo
    template_name = 'courses/courseinfo-delete.html'
    success_url = "/"

    def test_func(self):
        return True


""""""

def CourseObjectsHome(request):


    context = {
        'courseobjects': Course.objects.all()
    }

    return render(request, 'courses/courseobjects_user.html', context)


class CourseObjectListView(ListView):
    model = Course
    template_name = 'courses/courseobjects.html'
    context_object_name = 'courseobjects'
    # ordering = ['-date_posted']


class CourseObjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['start_date', 'end_date', 'course_info']
    template_name = 'courses/courseobject-create.html'
    context_object_name = 'courseobjects'

    def test_func(self):
        return True

    def form_valid(self, form):
        return super().form_valid(form)

class CourseObjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    template_name = 'courses/courseobject-create.html'
    context_object_name = 'courseobjects'

    def test_func(self):
        return True

    def form_valid(self, form):
        form.instance.recipient = self.request.user
        return super().form_valid(form)

class CourseObjectDetailView(DetailView):
    model = Course

class CourseObjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CourseInfo
    template_name = 'courses/courseinfo-delete.html'
    success_url = "/"

    def test_func(self):
        return True

    def form_valid(self, form):
        form.instance.recipient = self.request.user
        return super().form_valid(form)




""""""


def Scheduleitem(request):

    scheduleItem_form = ScheduleItemForm
    trainer_form = TrainerForm



    if request.method == 'POST':


        scheduleItem_form = ScheduleItemForm(request.POST)
        trainer_form = TrainerForm(request.POST)



        if trainer_form.is_valid() and scheduleItem_form.is_valid():

            scheduleItem_obj = scheduleItem_form.save(commit=False)
            trainer_obj = trainer_form.save(commit=False)

            overlap_check = []
            overlap_check.append(scheduleItem_obj.start)

            overlap_check.append(scheduleItem_obj.end)

            overlap_check.append(scheduleItem_obj.course.start_date)

            overlap_check.append(scheduleItem_obj.course.end_date)


            if overlap_check[0] < overlap_check[1] and overlap_check[2] <= overlap_check[0] and overlap_check[3] >= overlap_check[1] :

                scheduleItem_obj.save()
                trainer_obj = trainer_form.save(commit=False)
                trainer_obj.schedule = scheduleItem_obj

                trainer_obj.save()

                return redirect( 'userlist')

            else:
                scheduleItem_form = ScheduleItemForm()
                trainer_form = TrainerForm()

        else:
            scheduleItem_form = ScheduleItemForm()
            trainer_form = TrainerForm()





    return render(request, 'courses/scheduleitem-create.html', {'scheduleItem_form' : scheduleItem_form, 'trainer_form' : trainer_form})



def ScheduleItemHome(request,username):

    trainerItems = Trainer.objects.all()
    fuser = User.objects.get(username=username)


    x = []
    strained = 0
    days = 30

    for item in trainerItems:
        if fuser == item.user:
            dateItemStart = datetime.strptime(item.schedule.start.strftime("%Y/%m/%d"), "%Y/%m/%d" )
            dateItemEnd = datetime.strptime(item.schedule.end.strftime("%Y/%m/%d"), "%Y/%m/%d" )
            x.append(abs((dateItemStart - dateItemEnd).days))

    for element in x:
        strained += (2/math.pi)*math.atan(element/days)


    strained = round(strained, 2)

    context = {
        'traineritems': trainerItems,
        'strain' : strained,
        'fuser': fuser
    }

    return render(request, 'courses/scheduleitems.html', context)
