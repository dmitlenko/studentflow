from django.contrib import admin
from .models import PostCommentModel, PostModel, UserProfile

# Register your models here.
admin.site.register([PostCommentModel, PostModel, UserProfile])