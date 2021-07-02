from django.urls import path
from .views import (CommentLike, DeletePost, EditPost, LikedListPosts, ListPosts, MyPosts, PostLike, ReplyCreateView, ReplyLike,
                    SeePostDetails,
                    MakePost,
                    EditPost,
                    ReplyCreateView, search_forum, PopularListPosts
                    )
from . import views

urlpatterns = [
    path('', ListPosts.as_view(), name='forum-landing'),
    # pk is the primary key, so for example the first post has id = 1
    path('post/<int:pk>/', SeePostDetails.as_view(), name='individual-post'),
    path('post/make/', MakePost.as_view(), name='make-post'),
    path('post/<int:pk>/edit/', EditPost.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete-post'),


    path('comment/<int:ck>/like', CommentLike.as_view(), name='like-comment'),
    path('reply/<int:rk>/like', ReplyLike.as_view(), name='like-reply'),

    path('post/<int:pk>/like/', PostLike.as_view(), name='like-post'),


    path('post/<int:pk>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    path('myposts/', MyPosts.as_view(), name='my-posts'),
    path('search/', views.search_forum, name='forum-search'),
    path('top/', LikedListPosts.as_view(), name='post-sort-like'),
    path('popular/', PopularListPosts.as_view(), name='post-sort-popular'),






]
