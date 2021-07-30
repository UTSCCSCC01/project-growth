from django.db import models
from django.utils import timezone, tree
#from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from courses.models import CourseInfo



class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    video = models.FileField(null=True, blank=True, upload_to='videos/')
    course = models.ForeignKey(CourseInfo, on_delete=models.SET_NULL, null=True, blank=True, primary_key=False) # null=True

    #have a reactions thing here, like an int form 1 to 6 or a upvote downvote

    #how it will be printed out
    def __str__(self):
        return self.title

    #redirect actually redirects
    #reverse returns full url as string
    def get_absolute_url(self):
        #refer to forum/urls.py
        return reverse('forum-landing')
    #Success_url method to go to home page instead

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    likes= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')


    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('forum-landing')
        #refer to forum/urls.py
        #return reverse('individual-post', kwargs={'pk': self.post.id})

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='reply_likes')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        #refer to forum/urls.py
        return reverse('forum-landing')
        #return reverse('individual-post', kwargs={'pk': self.comment.post.pk})

    @property
    def get_replies(self):
        return self.replies.all()


#Notes on how to run a query to this model
# >>> from django.conf import settings
# >>> from forum.models import Post
# >>> from django.contrib.auth.models import User
# >>> from django.contrib.auth import get_user_model
# >>> get_user_model().objects.all()
# <QuerySet [<User: cydy8001>, <User: 860119817>, <User: student1>, <User: SahotaJai>]>
# >>> user = get_user_model().objects.filter(username='SahotaJai').first()