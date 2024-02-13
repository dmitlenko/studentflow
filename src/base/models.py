from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.db.models import Count
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rolepermissions.checkers import has_role
from studentflow.roles import Teacher

from os import path
from .validators import validate_file_size

class PostTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def order_by_post_count(self):
        return self.objects.annotate(post_count=Count('post')).order_by('-post_count')


def image_user_directory_path(instance, filename):
    return 'data/user_{0}/image/{1}'.format(instance.id, filename)

class User(AbstractUser):
    name = models.CharField('Ім\'я профілю',max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField('Фото', default='default_user.png', upload_to=image_user_directory_path, null=True, validators=[validate_file_size])
    image_banner = models.ImageField('Фон профілю', blank=True, upload_to=image_user_directory_path, null=True, validators=[validate_file_size])
    bio = models.TextField('Біографія', null=True, blank=True)

    review_topics = models.ManyToManyField(PostTopic, verbose_name='Теми перевірки', related_name='review_topics', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name if self.name else self.username

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def assign_review_topics(sender, instance=None, created=False, **kwargs):
    if created and has_role(instance, Teacher):
        instance.review_topics.add(*PostTopic.objects.all())

@receiver(post_save, sender=PostTopic)
def assign_new_topic(sender, instance=None, created=False, **kwargs):
    if created:
        for user in User.objects.all():
            if has_role(user, Teacher):
                user.review_topics.add(instance)
                user.save()

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

    published = models.BooleanField('Опублікувати', default=False)
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