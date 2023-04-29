from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm

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
        
        return render(request, self.template_name, {'form':AuthenticationForm})
    
    def post(self, request): 
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Authorization successful")

                return redirect('index_view')
        
        messages.error(request, "Unsuccessful authentication. Invalid information.")

        return redirect('login_view')
    
class RegistrationView(View):
    template_name = 'base/registration_view.html'

    def get(self, request, form:RegistrationForm=None):
        if request.user.is_authenticated:
            return redirect('index_view')
        
        if form is None:
            form = RegistrationForm

        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")    
            return redirect('index_view')
        
        messages.error(request, "Unsuccessful registration. Invalid information.")

        return self.get(request, form)


# FIXME: maybe this is a bad practice to mix class-base views and function-base views
def logout_view(request):
    logout(request)
    return redirect('index_view')