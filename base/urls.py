from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# url patterns for the base app
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('auth/signup/<int:role>', views.SignupView.as_view(), name='signup'),

    path('post/create', views.PostCreateView.as_view(), name='create_post'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='detail_post'),
    path('post/stats/<int:pk>', views.PostStatsView.as_view(), name='stats_post'),
    path('post/deletecomment/<int:pk>', views.PostCommentDeleteView.as_view(), name='delete_comment'),
    path('post/like/<int:pk>', views.LikePostView.as_view(), name='like_post'),
    path('post/unlike/<int:pk>', views.UnlikePostView.as_view(), name='unlike_post'),

    path('profile/detail/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.UserUpdateView.as_view(), name='update_profile'),

    path('user/follow/<int:pk>', views.UserFollowView.as_view(), name='follow_user'),
    path('user/unfollow/<int:pk>', views.UserUnfollowView.as_view(), name='unfollow_user'),

    path('user/files/', views.UserFilesView.as_view(), name='files'),
    path('user/files/upload/', views.UploadUserFileView.as_view(), name='upload_file'),
    path('user/files/delete/<int:pk>', views.DeleteUserFileView.as_view(), name='delete_file'),

    path('post/admin/unpublished/', views.UnpublishedPostListView.as_view(), name='unpublished_posts'),
    path('post/admin/publish/<int:pk>', views.PublishPostView.as_view(), name='publish_post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)