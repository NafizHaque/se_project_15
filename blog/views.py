from django.shortcuts import render ,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    )
from .models import Post
from .models import Qualifications
from .forms import ContactForm
from django.contrib import messages

# Create your views here.

class HomeView(TemplateView):
    template_name = 'blog/home.html'


    def get(self, request):
        admin_contact_form = ContactForm()
        context = {
            'posts' : Post.objects.all(),
            'admin_contact_form' : admin_contact_form

        }

        return render(request, self.template_name ,context)


    def post(self, request):

        admin_contact_form = ContactForm(request.POST)

        if admin_contact_form.is_valid():
            contact = admin_contact_form.save(commit=False)
            contact.author = request.user
            contact.save()
            firstn = admin_contact_form.cleaned_data['firstn']
            lastn = admin_contact_form.cleaned_data['lastn']
            email = admin_contact_form.cleaned_data['email']
            enquiry = admin_contact_form.cleaned_data['enquiry']
            content = admin_contact_form.cleaned_data['content']
            return redirect('blog-home')

        context = {
                    'posts' : Post.objects.all(), 
                    'admin_contact_form' : admin_contact_form, 
                    'firstn' : firstn, 
                    'lastn' : lastn, 
                    'email' : email, 
                    'enquiry' : enquiry, 
                    'content' : content
                } 
    
        return render(request, self.template_name ,context)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView( ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5 

    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields =['title', 'content', 'recipient']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields =['title', 'content']

    def test_func(self):
        post = self.get_object ()
        if self.request.user == post.recipient:
            return True
        return False


    def form_valid(self, form):
        form.instance.recipient = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    
    def test_func(self):
        post = self.get_object ()
        if self.request.user == post.recipient:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title' : 'About!'})

def links(request):
    return render(request, 'blog/links.html', {'title' : 'links!'})


def qualification(request):
    return render(request, 'blog/qualification.html', {'title' : 'Quali!'})


class NotificationView(ListView):
    model = Post
    template_name = 'blog/notification.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class QualificationView(ListView):
    model = Qualifications
    template_name = 'blog/qualification.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'qualifications'
    ordering = ['-date_posted']
    paginate_by = 5

class PostQualificationView(LoginRequiredMixin, CreateView):
    model = Qualifications
    fields =['title' , 'recipient']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QualificationDetailView(DetailView):
    model = Qualifications


class QualificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Qualifications
    success_url = "/"
    
    def test_func(self):
        qualification = self.get_object ()
        if self.request.user == qualification.recipient:
            return True
        return False