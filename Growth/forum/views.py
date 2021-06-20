from django.shortcuts import render
from django.http import HttpResponse
from .models import Post #this means import from the model.py of forum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

#might want to use @login_required in here to restrict acess to users.

#should decide which view to use: ListView, FormView, RecycleView

#forum in the path refers to templates/forum.
#in HTML it will be called like this {% for post in posts %}
#'posts' is the key for dictionary
#if we use as the third arguement {'user': 'john'} we could make specific titles for specifc users

class ListPosts(ListView):
    model = Post
    template_name = 'forum/forum.html' #<appName>/<model>_<viewtype>.html
    context_object_name = 'posts'

    #this will be minipulated when using filters, 
    #the minus means decending order
    #Change this ordering to by likes when you sort by best
    ordering = ['-date_posted'] 

class SeePostDetails(DetailView):
    model = Post
    #for automatic html detection use this format: <appName>/<model>_<viewtype>.html

class MakePost(LoginRequiredMixin , CreateView):
    model = Post
    fields = ['title', 'text']
    #this links to post_from.html automatically  
    # Note: this autmatically has a default form that it passes to the above html
    #overiding the default method 
    

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)  

    # def get_absolute_url(self): # new
    #     return reverse('post_detail', args=[str(self.id)])

class EditPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    #this links to post_from.html automatically  
    # Note: this autmatically has a default form that it passes to the above html
    #overiding the default method 
    

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)  
    
    def test_func(self):
        my_post = self.get_object() #gets the post

    # checks if the poster's user same as the one logged in
        if my_post.username == self.request.user: 
            return True
        return False

class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/forum'
    def test_func(self):
        my_post = self.get_object() #gets the post
        if my_post.username == self.request.user: 
            return True
        return False











