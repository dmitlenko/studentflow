from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        context = {}

        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'base/login_view.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index_view')

        context = {}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('index_view')
        else:
            return redirect('login_view')


# FIXME: maybe this is a bad practice to mix class-base views and function-base views
def logout_view(request):
    logout(request)
    return redirect('index_view')