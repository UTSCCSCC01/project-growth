from django.contrib import admin
from .models import Post, Comment, Reply

# Register your models here. to make them show on admin page
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)