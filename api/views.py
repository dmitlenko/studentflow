from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Post
from rest_framework.permissions import IsAuthenticated

class LikePostAPIView(APIView, IsAuthenticated):
    def post(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)


class UnlikePostAPIView(APIView, IsAuthenticated):
    def post(self, request, pk):
        post_to_like = get_object_or_404(Post, pk=pk)
        post_to_like.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)