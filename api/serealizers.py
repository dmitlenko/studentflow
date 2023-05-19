from rest_framework.serializers import ModelSerializer
from base.models import PostComment, User

class UserDataSerealizer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'first_name', 'last_name', 'last_login', 'date_joined')


class PostCommentSerializer(ModelSerializer):
    author = UserDataSerealizer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'body', 'date_created', 'author']