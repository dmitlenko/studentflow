from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, PostForm, UserForm
from .models import Post, PostComment, User
from django.urls import reverse_lazy, reverse
from datetime import datetime


class IndexView(ListView):
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post

    # def get(self, request):
    #     posts = Post.objects.all().order_by('-date_created')[:10]

    #     return render(request, self.template_name, {'posts': posts})


class LoginView(View):
    template_name = 'base/auth/login.html'

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return redirect('home')

        if form is None:
            form = AuthenticationForm()

        return render(request, self.template_name, {'form': form})

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

        messages.error(
            request, "Unsuccessful authentication. Invalid information.")

        return self.get(request, form)


class SignupView(View):
    template_name = 'base/auth/signup.html'

    def get(self, request, form: RegistrationForm = None):
        if request.user.is_authenticated:
            return redirect('home')

        if form is None:
            form = RegistrationForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('home')

        messages.error(
            request, "Unsuccessful registration. Invalid information.")

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
        self.success_url = reverse('detail_post', kwargs={
                                   'pk': self.kwargs['pk']})
        if request.user != obj.author:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj


class PostCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = PostComment
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        self.success_url = reverse('detail_post', kwargs={
                                   'pk': self.kwargs['pk']})
        if request.user != obj.author:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'base/post.html'
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = PostComment.objects.filter(
            post=self.get_object()).order_by('-date_created')
        return context

    def post(self, request, **kwargs):
        comment = PostComment.objects.create(
            author=request.user,
            post=self.get_object(),
            body=request.POST.get('body'),
        )

        return redirect(reverse('detail_post', kwargs={'pk': self.kwargs['pk']}))


class ProfileView(DetailView):
    model = User
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_count'] = PostComment.objects.filter(
            author=self.get_object()).count()
        context['posts'] = Post.objects.filter(author=self.get_object())
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'base/form/user.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj:
            return self.handle_no_permission()
        
        self.success_url = reverse('profile', kwargs={
                                   'pk': self.kwargs['pk']})

        return super().dispatch(request, *args, **kwargs)


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk == request.user.id:
            return redirect('home')
        
        try:
            user = User.objects.get(id=pk)
        except:
            return redirect('home')

        if request.user.following.filter(id=pk).count() == 0:
            request.user.following.add(user)
        else:
            # TODO: add "already following error"
            pass
        
        return redirect(reverse('profile', kwargs={'pk': self.kwargs['pk']}))

class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk == request.user.id:
            return redirect('home')
        
        try:
            user = User.objects.get(id=pk)
        except:
            return redirect('home')

        if request.user.following.filter(id=pk).count() >= 1:
            request.user.following.remove(user)
        else:
            # TODO: add "not following error"
            pass
        
        return redirect(reverse('profile', kwargs={'pk': self.kwargs['pk']}))
        

class FeedView(LoginRequiredMixin,ListView):
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author__in=self.request.user.following.all())

# FIXME: maybe this is a bad practice to mix class-base views and function-base views
def logout_view(request):
    logout(request)
    return redirect('home')
