from django.urls import path, include
from .views import LikePostAPIView, UnlikePostAPIView

urlpatterns = [
    path('post/<int:pk>/like', LikePostAPIView.as_view(), name='api_like_post'),
    path('post/<int:pk>/unlike', UnlikePostAPIView.as_view(), name='api_unlike_post'),

    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
