from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat/home.html'

    def get(self, request):
        return render(request, self.template_name, {})
