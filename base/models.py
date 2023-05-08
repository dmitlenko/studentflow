from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from os import path
from .validators import validate_file_size

# Create your models here.
def image_user_directory_path(instance, filename):
    return 'data/user_{0}/image/{1}'.format(instance.id, filename)

class User(AbstractUser):
    name = models.CharField('Ім\'я',max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField('Фото', default='default_user.png', upload_to=image_user_directory_path, null=True, validators=[validate_file_size])
    bio = models.TextField('Біографія', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name if self.name else self.username


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
    file = models.FileField('Файл',upload_to=user_directory_path, validators=[validate_file_size])
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return path.basename(self.file.name)


class PostTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

def post_user_directory_path(instance, filename):
    return 'data/user_{0}/post/{1}'.format(instance.author.id, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=150)
    body = models.TextField('Тіло')
    topic = models.ForeignKey(PostTopic, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    views = models.ManyToManyField(User, related_name='views')
    likes = models.ManyToManyField(User, related_name='likes')

    image = models.ImageField('Фото', upload_to=post_user_directory_path, null=True, blank=True, validators=[validate_file_size])
    files = models.ManyToManyField(UserFile, related_name='files', blank=True)

    reviewed = models.BooleanField('Перевірено', default=False)

    published = models.BooleanField('Опубліковане', default=False)
    date_published = models.DateTimeField('Дата публікації', default=now)
    
    archived = models.BooleanField('Архівовано', default=False)
    date_archive = models.DateTimeField('Дата архівації', blank=True, null=True)

    pinned = models.BooleanField('Закріпити',default=False)
    date_unpinned = models.DateTimeField('Дата й час відкріплення', blank=True, null=True)

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