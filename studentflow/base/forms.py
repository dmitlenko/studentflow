from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, UserFile, PostTopic


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    files = forms.ModelMultipleChoiceField(
        label='Файли',
        required=False,
        queryset=UserFile.objects.none())

    date_unpinned = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), required=False, label='Дата відкріплення')
    date_published = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), required=False, label='Дата публікації')
    date_archive = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), required=False, label='Дата архівації')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['files'].queryset = UserFile.objects.filter(uploader=self.request.user)


    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'likes', 'views', 'topic','reviewed']


class UserForm(forms.ModelForm):
    review_topics = forms.ModelMultipleChoiceField(PostTopic.objects, label='Тематики для розбору', required=False)

    class Meta:
        model = User
        fields = ['name', 'username','first_name', 'last_name', 'image', 'image_banner', 'review_topics', 'bio']