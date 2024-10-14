from django.urls import path, include
from .views import *

urlpatterns = [
    path('like/<int:pk>/', LikePostAPIView.as_view(), name='api_like_post'),
    
    path('post/<int:pk>/comments', ListCommentsAPIView.as_view(), name='api_post_comments'),
    path('post/<int:pk>/approve', ApprovePostAPIView.as_view(), name='api_approve_post'),
    path('post/<int:pk>/files', ListFilesAPIView.as_view(), name='api_post_files'),

    path('comment/<int:pk>/', CreateCommentAPIView.as_view(), name='api_comment_post'),

    path('follow/<int:pk>/', FollowUserAPIView.as_view(), name='api_follow_user'),

    path('chat/<int:pk>/messages', ListChatGroupMessagesAPIView.as_view(), name='api_chat_messages'),

    path('stats/posts', PostsStatisticsAPIView.as_view(), name='api_stat_posts'),
    path('stats/users', UsersStatisticsAPIView.as_view(), name='api_stat_users'),

    path('login/<str:token>', TokenAuthAPIView.as_view(), name='api_login'),
]
