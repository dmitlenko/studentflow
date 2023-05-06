from re import search as re_search
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, PostForm, UserForm
from .models import Post, PostComment, User, UserFollow, PostTopic
from django.urls import reverse_lazy, reverse
from .utlis import search_posts

class IndexView(ListView):
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = PostTopic.objects.all()
        return context

    def get_queryset(self):
        return search_posts(Post.objects.all(), self.request.GET.get('q'))


class LoginView(View):
    template_name = 'base/auth/login.html'

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return redirect('home')

        if form is None:
            form = AuthenticationForm()

        return render(request, self.template_name, {'form': form, 'is_auth':True})

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

    def get(self, request, role, form: RegistrationForm = None):
        if request.user.is_authenticated:
            return redirect('home')

        if form is None:
            form = RegistrationForm()

        return render(request, self.template_name, {'form': form, 'is_auth':True, 'role':role})

    def post(self, request, role):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save(role=role)
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

        if super().form_valid(form):
            self.object = form.save(commit=False)
            topic_name = self.request.POST.get('topic')
            topic, created = PostTopic.objects.get_or_create(name=topic_name)
            self.object.topic = topic
            self.object.save()

            return redirect(reverse('detail_post', kwargs={'pk':self.object.id}))

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['topics'] = PostTopic.objects.all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'base/form/post.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['topics'] = PostTopic.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if super().form_valid(form):
            self.object = form.save(commit=False)
            topic_name = self.request.POST.get('topic')
            topic, created = PostTopic.objects.get_or_create(name=topic_name)
            self.object.topic = topic
            self.object.save()

            return redirect(reverse('detail_post', kwargs={'pk':self.object.id}))

        return False


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj


class PostCommentDeleteView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, pk):
        obj = get_object_or_404(PostComment, pk=pk)

        if self.request.user != obj.author and obj.post.author != self.request.user:
            return self.handle_no_permission()
        
        obj.delete()
        return self.request.META.get('HTTP_REFERER')


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
    
    def dispatch(self, request, *args, **kwargs):
        self.get_object().views.add(request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        comment = PostComment.objects.create(
            author=request.user,
            post=self.get_object(),
            body=request.POST.get('body'),
        )

        return redirect(reverse('detail_post', kwargs={'pk': self.kwargs['pk']}) + f'#comment_{comment.id}')


class ProfileView(DetailView):
    model = User
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_count'] = PostComment.objects.filter(
            author=self.get_object()).count()
        context['posts'] = Post.objects.filter(author=self.get_object())
        return context


class PostStatsView(DetailView):
    model = Post
    template_name = 'base/post_stats.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)


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


class UserFollowView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        user_to_follow = get_object_or_404(User, id=self.kwargs.get('pk'))
        UserFollow.objects.get_or_create(user=user_to_follow, follower=self.request.user)
        return reverse_lazy('profile', kwargs={'pk': user_to_follow.id})


class UserUnfollowView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, id=self.kwargs.get('pk'))
        UserFollow.objects.filter(user=user_to_unfollow, follower=self.request.user).delete()
        return reverse_lazy('profile', kwargs={'pk': user_to_unfollow.id})
        

class FeedView(LoginRequiredMixin, ListView):
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = PostTopic.objects.all()
        return context

    def get_queryset(self):
        current_user = self.request.user
        followed_users = UserFollow.objects.filter(follower=current_user).values_list('user', flat=True)
        posts = Post.objects.filter(author__in=followed_users)
        return search_posts(posts, self.request.GET.get('q'))


class LikePostView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        post_to_like = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        post_to_like.likes.add(self.request.user)
        return self.request.META.get('HTTP_REFERER') + f'#post_{post_to_like.id}'


class UnlikePostView(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def get_redirect_url(self, *args, **kwargs):
        post_to_like = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        post_to_like.likes.remove(self.request.user)
        return self.request.META.get('HTTP_REFERER') + f'#post_{post_to_like.id}'


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)