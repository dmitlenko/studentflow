from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'likes', 'views']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'image', 'bio']
