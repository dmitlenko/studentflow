from django.contrib import admin
from .models import PostComment, Post, UserProfile

# Register your models here.
admin.site.register([PostComment, Post, UserProfile])