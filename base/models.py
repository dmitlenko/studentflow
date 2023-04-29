from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.png', upload_to='profile_pics', null=True)
    bio = models.CharField(max_length=2000, null=True)


class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    # TODO: Add ability to upload images for the post
    # image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date_created']


class PostCommentModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)