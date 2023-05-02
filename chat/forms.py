from django import forms
from .models import ChatGroup

class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = '__all__'
        exclude = ['creator', 'private']