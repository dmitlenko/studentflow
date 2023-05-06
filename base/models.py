from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    class Role(models.IntegerChoices):
        STUDENT = 1, 'Студент'
        TEACHER = 2, 'Викладач'

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField(default='default_user.png', upload_to='images/profile', null=True, validators=[validate_image], blank=True)
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

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    views = models.ManyToManyField(User, related_name='views')
    likes = models.ManyToManyField(User, related_name='likes')

    pinned = models.BooleanField(default=False)

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    image = models.ImageField(upload_to='images/post', null=True, blank=True, validators=[validate_image])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()

        if not self.image.name:
            return
        
        img = Image.open(self.image.path)
        new_width, new_height = 1200, 560

        if img.height > new_height or img.width > new_width:
            width, height = img.size
            
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2

            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

    class Meta:
        ordering = ['-pinned','-date_created']


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body