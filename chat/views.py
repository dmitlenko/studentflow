from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatGroup, ChatGroupMessage
from .forms import ChatGroupForm

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
        

class UpdateChatGroupView(LoginRequiredMixin, UpdateView):
    model = ChatGroup
    template_name = 'chat/form/update.html'
    login_url = 'login'
    form_class = ChatGroupForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, **kwargs):
        obj = self.get_object()

        self.success_url = reverse('chat', kwargs={
                                   'pk': self.kwargs['pk']})

        if request.user != obj.creator:
            return self.handle_no_permission()
        
        return super().dispatch(request, **kwargs)
    

class CreateChatGroupView(LoginRequiredMixin, CreateView):
    model = ChatGroup
    template_name = 'chat/form/update.html'
    login_url = 'login'
    form_class = ChatGroupForm
    success_url = reverse_lazy('chat_home')
