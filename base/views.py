from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, PostForm
from .models import Post
from django.urls import reverse_lazy

class IndexView(View):
    template_name = 'base/home.html'

    def get(self, request):
        posts = Post.objects.all().order_by('-date_created')[:10]

        return render(request, self.template_name, {'posts':posts})


class LoginView(View):
    template_name = 'base/auth/login.html'

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return redirect('home')
        
        if form is None:
            form = AuthenticationForm()
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request): 
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Authorization successful")

                return redirect('home')
        
        messages.error(request, "Unsuccessful authentication. Invalid information.")

        return self.get(request, form)
    
class SignupView(View):
    template_name = 'base/auth/signup.html'

    def get(self, request, form:RegistrationForm=None):
        if request.user.is_authenticated:
            return redirect('home')
        
        if form is None:
            form = RegistrationForm()

        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")    
            return redirect('home')
        
        messages.error(request, "Unsuccessful registration. Invalid information.")

        return self.get(request, form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'base/form/post.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'base/form/post.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'base/form/delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs )
        context['obj'] = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return context


# FIXME: maybe this is a bad practice to mix class-base views and function-base views
def logout_view(request):
    logout(request)
    return redirect('home')