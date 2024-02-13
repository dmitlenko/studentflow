from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, PostForm, UserForm
from .models import Post, PostComment, User, UserFollow, PostTopic, UserFile
from django.urls import reverse_lazy, reverse
from .utils import search_posts
from django.db.models import Q, Count, Sum
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from studentflow.roles import Teacher, Student
from chat.models import ChatGroup, ChatGroupMessage
from .mixins import PageTitleViewMixin

class IndexView(PageTitleViewMixin, ListView):
    title = 'Головна'
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = list(PostTopic.order_by_post_count())
        return context

    def get_queryset(self):
        return search_posts(Post.objects.filter(published=True, reviewed=True, archived=False), self.request.GET)


class SigninView(PageTitleViewMixin, FormView):
    title = 'Авторизація'
    template_name = 'base/auth/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_auth'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home')

        return valid


class SignupView(PageTitleViewMixin, CreateView):
    title = 'Реєстрація'
    model = User
    template_name = 'base/auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_auth'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)

        login(self.request, self.object)

        assign_role(self.object, Teacher if self.kwargs['role'] == Teacher.id else Student)

        return valid


class PostCreateView(PageTitleViewMixin, LoginRequiredMixin, CreateView):
    title = 'Створення оголошення'
    model = Post
    form_class = PostForm
    template_name = 'base/form/post.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user

        if super().form_valid(form):
            self.object = form.save(commit=False)
            topic_name = self.request.POST.get('topic')
            topic, created = PostTopic.objects.get_or_create(name=topic_name)
            self.object.topic = topic
            if has_role(self.request.user, Teacher):
                self.object.reviewed = True
            self.object.save()

            return redirect(reverse('detail_post', kwargs={'pk':self.object.id}))

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['topics'] = PostTopic.objects.all()
        return context


class PostUpdateView(PageTitleViewMixin, LoginRequiredMixin, UpdateView):
    title = 'Редагування оголошення'
    model = Post
    form_class = PostForm
    template_name = 'base/form/post.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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

        return super().form_invalid(form)


class PostDeleteView(PageTitleViewMixin, LoginRequiredMixin, DeleteView):
    title = 'Видалення оголошення'
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj


class PostDetailView(PageTitleViewMixin, LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'base/post.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = PostComment.objects.filter(
            post=self.get_object()).order_by('-date_created')
        return context
    
    def get_title(self):
        return self.get_object().title

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not obj.reviewed and (self.request.user != obj.author and not has_role(self.request.user, Teacher)):
            return self.handle_no_permission()

        if obj.reviewed and obj.published and not obj.archived:
            obj.views.add(request.user)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        comment = PostComment.objects.create(
            author=request.user,
            post=self.get_object(),
            body=request.POST.get('body'),
        )

        return redirect(reverse('detail_post', kwargs={'pk': self.kwargs['pk']}) + f'#comment_{comment.id}')


class ProfileView(PageTitleViewMixin, DetailView):
    model = User
    template_name = 'base/profile.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_title(self):
        return self.get_object().username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published=True, reviewed=True, archived=False, author=self.get_object())
        return context


class PostStatsView(PageTitleViewMixin, DetailView):
    title = 'Статистика оголошення'
    model = Post
    template_name = 'base/post_stats.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(PageTitleViewMixin, LoginRequiredMixin, UpdateView):
    title = 'Редагування профілю'
    model = User
    form_class = UserForm
    template_name = 'base/form/user.html'
    success_url = reverse_lazy('home')

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
        

class FeedView(PageTitleViewMixin, LoginRequiredMixin, ListView):
    title = 'Підписки'
    template_name = 'base/home.html'
    paginate_by = 6
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = list(PostTopic.order_by_post_count())
        return context

    def get_queryset(self):
        current_user = self.request.user
        followed_users = UserFollow.objects.filter(follower=current_user).values_list('user', flat=True)
        posts = Post.objects.filter(reviewed=True, archived=False, published=True, author__in=followed_users)
        return search_posts(posts, self.request.GET)


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserFilesView(PageTitleViewMixin, LoginRequiredMixin, ListView):
    title = 'Файли користувача'
    model = UserFile
    template_name = 'base/file_list.html'

    def get_queryset(self):
        return UserFile.objects.filter(uploader=self.request.user)


class UploadUserFileView(PageTitleViewMixin, LoginRequiredMixin, CreateView):
    title = 'Завантаження файлу'
    model = UserFile
    template_name = 'base/form/file.html'
    login_url = 'login'
    success_url = reverse_lazy('files')
    fields = ['file']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        if self.request.user.userfile_set.count() >= 20:
            form.add_error('file', 'Ви вже завантажили 20 файлів!')
            return super().form_invalid(form)

        return super().form_valid(form)


class DeleteUserFileView(PageTitleViewMixin, LoginRequiredMixin, DeleteView):
    title = 'Видалення файлу'
    model = UserFile
    template_name = 'delete.html'
    success_url = reverse_lazy('files')
    login_url = 'login'

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        if obj.uploader != self.request.user:
            return self.handle_no_permission()
        return obj


class ReviewPostListView(PageTitleViewMixin, HasRoleMixin, ListView):
    title = 'Перевірка оголошень'
    allowed_roles = Teacher
    model = Post
    template_name = 'base/admin/unpublished_list.html'
    login_url = 'login'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Post.objects.filter(Q(reviewed=False))
        
        return Post.objects.filter(
            ~Q(author=self.request.user) 
            & Q(reviewed=False)
            & Q(author__is_staff=False)
            & Q(topic__in=self.request.user.review_topics.all())
        )


class GlobalStatsView(PageTitleViewMixin, HasRoleMixin, TemplateView):
    title = 'Загальна статистика'
    allowed_roles = Teacher
    template_name = 'base/admin/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_objects = Post.objects.all()
        user_objects = User.objects.all()
        chat_objects = ChatGroup.objects.filter(private=False)
        chat_messages_objects = ChatGroupMessage.objects.all()
        file_objects = UserFile.objects.all()

        context['most_liked_post'] = post_objects.annotate(likes_count=Count('likes')).order_by('-likes_count').first()
        context['most_viewed_post'] = post_objects.annotate(views_count=Count('views')).order_by('-views_count').first()
        context['latest_post'] = post_objects.order_by('-date_created').first()

        context['active_user'] = user_objects.annotate(num_posts=Count('post')).order_by('-num_posts').first()
        context['latest_user'] = user_objects.order_by('-date_joined').first()

        context['chat_count'] = chat_objects.count()
        context['chat_popular'] = chat_objects.annotate(participants_count=Count('participants')).order_by('-participants_count').first()
        context['chat_active'] = chat_objects.annotate(num_messages=Count('chatgroupmessage')).order_by('-num_messages').first()
        context['chat_messages_count'] = chat_messages_objects.count()

        context['file_count'] = file_objects.count()

        return context


class UserPostsListView(PageTitleViewMixin, LoginRequiredMixin, ListView):
    title = 'Список оголошень'
    model = Post
    template_name = 'base/admin/user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserLikesListView(PageTitleViewMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'base/admin/post_list.html'
    title = 'Список вподобаних оголошень'

    def get_queryset(self):
        return Post.objects.filter(likes=self.request.user)


class UserViewsListView(PageTitleViewMixin, LoginRequiredMixin, ListView):
    model = Post
    template_name = 'base/admin/post_list.html'
    title = 'Список переглянутих оголошень'

    def get_queryset(self):
        return Post.objects.filter(views=self.request.user)