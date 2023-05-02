from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatGroup, ChatGroupMessage

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat/home.html'

    def get(self, request):
        chats = [{
            'chat':chat,
            'last_message':chat.chatgroupmessage_set.last()
        } for chat in ChatGroup.objects.filter(participants=request.user)]

        return render(request, self.template_name, {
            'chats':chats
        })
