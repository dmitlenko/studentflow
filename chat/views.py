from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView
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


class ChatGroupView(LoginRequiredMixin, DetailView):
    model = ChatGroup
    template_name = 'chat/chat.html'
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.get_object().chatgroupmessage_set.all()
        return context
    
    def dispatch(self, request, **kwargs):
        obj = self.get_object()

        if request.user == obj.creator or request.user in obj.participants.all():
            return super().dispatch(request, **kwargs)
        else:
            return self.handle_no_permission()