from django.contrib import admin
from .models import ChatGroup, ChatGroupMessage

# Register your models here.
admin.site.register([ChatGroup, ChatGroupMessage])