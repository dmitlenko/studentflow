from django.urls import path, include
from .views import *

urlpatterns = [
    path('like/<int:pk>/', LikePostAPIView.as_view(), name='api_like_post'),
    
    path('post/<int:pk>/comments', ListCommentsAPIView.as_view(), name='api_post_comments'),

    path('comment/<int:pk>/', CreateCommentAPIView.as_view(), name='api_comment_post'),

    path('follow/<int:pk>/', FollowUserAPIView.as_view(), name='api_follow_user'),
]
