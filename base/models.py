from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.exceptions import ValidationError
from os import path
from .utils import validate_file_size

# Create your models here.
class User(AbstractUser):
    class Role(models.IntegerChoices):
        STUDENT = 1, 'Студент'
        TEACHER = 2, 'Викладач'

        
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField(default='default_user.png', upload_to='images/profile', null=True, validators=[validate_file_size], blank=True)
    bio = models.TextField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'follower'], name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f'{self.follower} -> {self.user}'


def user_directory_path(instance, filename):
    return 'data/user_{0}/{1}'.format(instance.uploader.id, filename)


class UserFile(models.Model):
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_size])
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return path.basename(self.file.name)


class PostTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    views = models.ManyToManyField(User, related_name='views')
    likes = models.ManyToManyField(User, related_name='likes')

    pinned = models.BooleanField(default=False)
    topic = models.ForeignKey(PostTopic, on_delete=models.SET_NULL, null=True)

    image = models.ImageField(upload_to='images/post', null=True, blank=True, validators=[validate_file_size])
    files = models.ManyToManyField(UserFile, related_name='files', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pinned','-date_created']


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body