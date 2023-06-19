from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Post, User, PostComment, UserFollow
from .serealizers import PostCommentSerializer, UserDataSerializer, UserFileSerializer
from rest_framework.permissions import IsAuthenticated
from rolepermissions.checkers import has_role
from studentflow.roles import Teacher
from rest_framework.authentication import TokenAuthentication
from chat.models import ChatGroup
from chat.serializers import ChatGroupMessageSerializer
from django.db.models import Count
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.urls import reverse

class LikePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)


class FollowUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, id=pk)
        UserFollow.objects.get_or_create(user=user_to_follow, follower=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_to_unfollow = get_object_or_404(User, id=pk)
        UserFollow.objects.filter(user=user_to_unfollow, follower=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class ListCommentsAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.postcomment_set.all()
        serealizer = PostCommentSerializer(comments, many=True)
        return Response(serealizer.data)


class ListFilesAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        files = post.files.all()
        serealizer = UserFileSerializer(files, many=True)
        return Response(serealizer.data)


class CreateCommentAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serealizer = PostCommentSerializer(data=request.data)
        if serealizer.is_valid():
            serealizer.save(author=request.user, post=post)
            return Response(serealizer.data, status=status.HTTP_201_CREATED)
        return Response(serealizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(PostComment, pk=pk)

        if request.user == comment.author or request.user == comment.post.author:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_403_FORBIDDEN)


class ApprovePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        if not has_role(request.user, Teacher):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        post = get_object_or_404(Post, pk=pk)
        post.reviewed = True
        post.save()
        
        return Response(status=status.HTTP_200_OK)


class ListChatGroupMessagesAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatGroupMessageSerializer

    def get(self, request, pk):
        chat_group = get_object_or_404(ChatGroup, pk=pk)

        if not (request.user == chat_group.creator or request.user in chat_group.participants.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)

        messages = chat_group.chatgroupmessage_set.all()
        serealizer =  ChatGroupMessageSerializer(messages, many=True)
        return Response(serealizer.data)


class PostsStatisticsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not has_role(request.user, Teacher):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        published_posts = Post.objects.filter(published=True).values('date_published__date').annotate(total=Count('id')).order_by('date_published__date')

        return Response([{
            'date': post['date_published__date'],
            'total': post['total']
        } for post in published_posts])
    

class UsersStatisticsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not has_role(request.user, Teacher):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.all().values('date_joined__date').annotate(total=Count('id')).order_by('date_joined__date')

        return Response([{
            'date': user['date_joined__date'],
            'total': user['total']
        } for user in users])
    

class TokenAuthAPIView(APIView):
    def get(self, request, token):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        login(request, get_object_or_404(Token, key=token).user)

        return redirect(reverse('home'))