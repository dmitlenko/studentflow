from django.urls import path, include
from .views import *

urlpatterns = [
    path('post/<int:pk>/like', LikePostAPIView.as_view(), name='api_like_post'),
    path('post/<int:pk>/unlike', UnlikePostAPIView.as_view(), name='api_unlike_post'),
    path('post/<int:pk>/comments', ListCommentsAPIView.as_view(), name='api_post_comments'),
    
    path('comment/<int:pk>/', CreateCommentAPIView.as_view(), name='api_comment_post'),

    path('users/<int:pk>/data', ListCommentsAPIView.as_view(), name='api_unlike_post'),

    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
