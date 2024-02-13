from django.contrib import admin
from .models import PostComment, Post, User, UserFollow, PostTopic, UserFile

# Register your models here.
admin.site.register([PostComment, Post, User, UserFollow, PostTopic, UserFile])