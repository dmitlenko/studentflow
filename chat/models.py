from base.models import User
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class ChatGroup(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, verbose_name='Учасники', related_name='participants', blank=True)
    image = models.ImageField('Фото', default='default_chatgroup.png', upload_to='images/groups', blank=True, validators=[validate_image])
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
