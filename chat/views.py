from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.base import RedirectView
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatGroup, ChatGroupMessage
from .forms import ChatGroupForm
from base.models import User
from django.db.models import Count

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

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

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

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DeleteChatGroupView(LoginRequiredMixin, DeleteView):
    model = ChatGroup
    template_name = 'delete.html'
    success_url = reverse_lazy('chat_home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def dispatch(self, request, **kwargs):
        obj = self.get_object()

        if request.user != obj.creator:
            return self.handle_no_permission()
        
        return super().dispatch(request, **kwargs)


class CreatePrivateChatView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return reverse('home')
        
        if user == self.request.user:
            return reverse('home')
        
        chat_group = ChatGroup.objects.filter(
            creator=None,
            private=True,
            participants__in=[user, self.request.user]
        ).annotate(num_participants=Count('participants')).filter(num_participants=2)

        if chat_group.exists():
            chat_group = chat_group.first()
        else:
            chat_group = ChatGroup.objects.create(
                name = f'Chat with @{self.request.user.username} and @{user.username}',
                private = True
            )
            chat_group.participants.add(self.request.user, user)

        return reverse('chat', kwargs={'pk': chat_group.id})