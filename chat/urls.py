from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view(), name='chat_home'),
    path('<int:pk>', ChatGroupView.as_view(), name='chat'),
    path('<int:pk>/update', UpdateChatGroupView.as_view(), name='chat_update')
]