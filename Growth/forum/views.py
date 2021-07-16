from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, request, HttpRequest
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import FormView
# this means import from the model.py of forum
from .models import Post, Comment, Reply
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from notificationsForum.signals import notify

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CommentForm, ReplyForm
from django.db.models import Q
from itertools import chain, groupby


# might want to use @login_required in here to restrict acess to users.

# should decide which view to use: ListView, FormView, RecycleView

# forum in the path refers to templates/forum.
# in HTML it will be called like this {% for post in posts %}
# 'posts' is the key for dictionary
# if we use as the third arguement {'user': 'john'} we could make specific titles for specifc users


def search_forum(request):
    if request.method == 'POST':
        searched = request.POST['ForumSearch']
        if searched != None and searched != '':
            posts = Post.objects.filter(Q(
                text__icontains=searched)| Q(
                title__icontains=searched))#| Q(username.username__icontains = searched))
            comments =  Comment.objects.filter(Q(
                text__icontains=searched))
            reply =  Reply.objects.filter(Q(
                text__icontains=searched))
            users = get_user_model().objects.filter(Q(
                username__icontains=searched))
            
            querychain = chain(posts, comments, reply, users)
            qs = sorted(querychain, key=lambda instance: instance.pk, reverse=True)
            return render(request, 'forum/my_search.html', context={'data': qs})
        else:
            return redirect('/forum/')
    else:
        return redirect('/forum/')


class ListPosts(ListView):
    model = Post
    template_name = 'forum/forum.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'posts'

    # this will be minipulated when using filters,
    # the minus means decending order
    # Change this ordering to by likes when you sort by best
    ordering = ['-date_posted']

class PopularListPosts(ListView):
    model = Post
    template_name = 'forum/forum.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'posts'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['posts'] = context['posts'].filter()\
        .annotate(comment_count = Count( ('comment')))\
        .order_by('-comment_count')
        return context

class LikedListPosts(ListView):
    model = Post
    template_name = 'forum/forum.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['posts'] = context['posts'].filter()\
        .annotate(likes_count=Count('likes'))\
        .order_by('-likes_count')
        return context

class MyPosts(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'forum/my_posts.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'posts'

    # this will be minipulated when using filters,
    # the minus means decending order
    # Change this ordering to by likes when you sort by best
    ordering = ['-date_posted']

class SeePostDetails(LoginRequiredMixin, DetailView, CreateView):
    model = Post

    template_name = 'forum/comment_mode.html'
    form_class = CommentForm
    success_url = '/forum'

    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))

        post = get_object_or_404(Post, id= self.kwargs.get('pk'))
        notify.send(sender=self.request.user, recipient=post.username, verb='NewComment', description=post)

        return super().form_valid(form)

    #form = CommentForm()
    #print( request.HttpRequest.body)

    #def post(self, request, pk, *args, **kwargs):
    # request = HttpRequest()
    # if request.POST.get('replyButton') is not None:
    #     commentID = int(request.POST.get('replyButton'))
    #if request.method == 'POST' and commentID >=0:
    #    print("button #"+commentID+" was clicked")
        # formReply = ReplyForm(request.POST)#, initial={
        #                       #'username': self.request.user, 'comment': Comment.objects.get(pk=commentID)})

        # if commentID >= 0:
        #     print(commentID)

        # def form_valid(self, formReply):
        #     formReply.instance.username = self.request.user
        #     formReply.instance.comment = Comment.objects.get(pk=int(request.POST.get('replyButton')))
        #     return super().form_valid(formReply)

       # reply = form.save()
        # print(reply)
    #      post = Post.objects.get(pk=pk)
    #      form = CommentForm()

    #      context = {
    #         'post': post,
    #         'form': form,
    #         'Rform': ReplyForm(),
    #     }

    #      return render(request, 'forum/post_detail.html', context)

    # def post(self, request, *args, **kwargs):
    #     return redirect('/forum/')

    #model = Comment

    # for automatic html detection use this format: <appName>/<model>_<viewtype>.html


class MakePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'video', 'course']
    # this links to post_from.html automatically
    # Note: this autmatically has a default form that it passes to the above html
    # overiding the default method

    success_url = '/forum'

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    # def get_absolute_url(self): # new
    #      return reverse('post_detail', args=[str(self.id)])


class EditPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'video', 'course']
    # this links to post_from.html automatically
    # Note: this autmatically has a default form that it passes to the above html
    # overiding the default method

    success_url = '/forum'

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        my_post = self.get_object()  # gets the post

    # checks if the poster's user same as the one logged in
        if my_post.username == self.request.user:
            return True
        return False


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/forum'

    def test_func(self):
        my_post = self.get_object()  # gets the post
        if my_post.username == self.request.user:
            return True
        return False


class ReplyCreateView(LoginRequiredMixin, DetailView, CreateView):
    model = Post

    template_name = 'forum/reply_mode.html'
    form_class = ReplyForm
    success_url = '/forum/'

#self.kwargs.get('sk')
    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.comment =  Comment.objects.get(pk=int(self.request.POST.get('replyButton')))
        comment = form.instance.comment


        #reply = get_object_or_404(Reply, id= self.kwargs.get('rk'))
        notify.send(sender=self.request.user, recipient=comment.username, verb='NewReply', description=comment.text)

        return super().form_valid(form)

class PostLike(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id= self.kwargs.get('pk'))
        current_user = self.request.user
     
        if current_user in post.likes.all():
            post.likes.remove(current_user)
        else:      
             post.likes.add(current_user)
             notify.send(sender=current_user, recipient=post.username, verb='LikePost', description=post)
        return post.get_absolute_url()

class CommentLike(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id= self.kwargs.get('ck'))
        current_user = self.request.user
     
        if current_user in comment.likes.all():
            comment.likes.remove(current_user)
        else:      
             comment.likes.add(current_user) # like on comment done.
             notify.send(sender=current_user, recipient=comment.username, verb='LikeComment', description=comment.text)
             
        return comment.get_absolute_url()


class ReplyLike(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id= self.kwargs.get('rk'))
        current_user = self.request.user
     
        if current_user in reply.likes.all():
            reply.likes.remove(current_user)
        else:      
             reply.likes.add(current_user)
             notify.send(sender=current_user, recipient=reply.username, verb='LikeReply', description=reply.text)
        return reply.get_absolute_url()
