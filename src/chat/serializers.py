from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ChatGroupMessage
from api.serealizers import UserDataSerializer

class ChatGroupMessageSerializer(ModelSerializer):
    author = UserDataSerializer(read_only=True)

    class Meta:
        model = ChatGroupMessage
        fields = ['author', 'body', 'date_created', 'chat_group']