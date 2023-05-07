from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, UserFile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, role, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.role = role
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    files = forms.ModelMultipleChoiceField(
        label='Файли',
        required=False,
        queryset=UserFile.objects.none())
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['files'].queryset = UserFile.objects.filter(uploader=self.request.user)

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'likes', 'views', 'topic']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'image', 'bio']