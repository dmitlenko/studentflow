from django import forms
from .models import ChatGroup
from base.models import User

class ChatGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(userfollow__follower=self.request.user)

    class Meta:
        model = ChatGroup
        fields = '__all__'
        exclude = ['creator', 'private']