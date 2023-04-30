from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default_user.png', upload_to='profile_pics', null=True)
    bio = models.CharField(max_length=2000, null=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

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
        ordering = ['date_created']


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)