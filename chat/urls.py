from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view(), name='chat_home'),
    path('create/', CreateChatGroupView.as_view(), name='chat_create'),
    path('<int:pk>', ChatGroupView.as_view(), name='chat'),
    path('<int:pk>/update', UpdateChatGroupView.as_view(), name='chat_update'),
    path('<int:pk>/delete', DeleteChatGroupView.as_view(), name='chat_delete'),
    path('with/<int:user_id>', CreatePrivateChatView.as_view(), name='chat_with')
]