from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Post, User, PostComment, UserFollow
from .serealizers import PostCommentSerializer, UserDataSerealizer
from rest_framework.permissions import IsAuthenticated

class LikePostAPIView(APIView, IsAuthenticated):
    def post(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)


class FollowUserAPIView(APIView, IsAuthenticated):
    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, id=pk)
        UserFollow.objects.get_or_create(user=user_to_follow, follower=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_to_unfollow = get_object_or_404(User, id=pk)
        UserFollow.objects.filter(user=user_to_unfollow, follower=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class ListCommentsAPIView(ListAPIView, IsAuthenticated):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.postcomment_set.all()
        serealizer = PostCommentSerializer(comments, many=True)
        return Response(serealizer.data)


class CreateCommentAPIView(CreateAPIView, IsAuthenticated):
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