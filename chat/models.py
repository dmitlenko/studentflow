from base.models import User
from django.db import models
from django.core.exceptions import ValidationError
from base.validators import validate_file_size

# Create your models here.
class ChatGroup(models.Model):        
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, verbose_name='Учасники', related_name='participants', blank=True)
    image = models.ImageField('Фото', default='default_chatgroup.png', upload_to='images/groups', blank=True, validators=[validate_file_size])
    description = models.CharField('Опис', max_length=2000, blank=True)
    name = models.CharField('Назва', max_length=200)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ChatGroupMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
