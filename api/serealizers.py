from rest_framework.serializers import ModelSerializer, SerializerMethodField
from base.models import PostComment, User, UserFile

class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'first_name', 'last_name', 'last_login', 'date_joined')


class UserFileSerializer(ModelSerializer):
    file_name = SerializerMethodField()
    file_path = SerializerMethodField()
    file_size = SerializerMethodField()
    uploader = UserDataSerializer(read_only=True)

    class Meta:
        model = UserFile
        fields = ['id', 'uploader', 'date_created', 'file_name', 'file_path', 'file_size']

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]

    def get_file_path(self, obj):
        return obj.file.name

    def get_file_size(self, obj):
        return obj.file.size


class PostCommentSerializer(ModelSerializer):
    author = UserDataSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'body', 'date_created', 'author']