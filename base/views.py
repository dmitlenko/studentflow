from django.shortcuts import render
from django.views import View


class MainView(View):
    template_name = 'index.html'

    def get(self, request):
        context = {}

        return render(request, self.template_name, context)