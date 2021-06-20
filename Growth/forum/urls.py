from django.urls import path
from .views import (DeletePost, EditPost, ListPosts,
                    SeePostDetails,
                    MakePost,
                    EditPost,
                    CommentCreateView
                    )
from . import views

urlpatterns = [
    path('', ListPosts.as_view(), name='forum-landing'),
    # pk is the primary key, so for example the first post has id = 1
    path('post/<int:pk>/', SeePostDetails.as_view(), name='individual-post'),
    path('post/make/', MakePost.as_view(), name='make-post'),
    path('post/<int:pk>/edit/', EditPost.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete-post'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
]
