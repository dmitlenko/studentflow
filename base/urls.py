from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# url patterns for the base app
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('auth/login', views.SigninView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('auth/signup/<int:role>', views.SignupView.as_view(), name='signup'),

    path('post/create', views.PostCreateView.as_view(), name='create_post'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='detail_post'),
    path('post/stats/<int:pk>', views.PostStatsView.as_view(), name='stats_post'),

    path('profile/detail/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.UserUpdateView.as_view(), name='update_profile'),

    path('user/files/', views.UserFilesView.as_view(), name='files'),
    path('user/files/upload/', views.UploadUserFileView.as_view(), name='upload_file'),
    path('user/files/delete/<int:pk>', views.DeleteUserFileView.as_view(), name='delete_file'),

    path('man/post/unpublished/', views.ReviewPostListView.as_view(), name='unpublished_posts'),
    path('man/stats/', views.GlobalStatsView.as_view(), name='global_stats'),
    path('man/post/list', views.UserPostsListView.as_view(), name='user_posts'),
    path('man/post/liked', views.UserLikesListView.as_view(), name='user_likes'),
    path('man/post/viewed', views.UserViewsListView.as_view(), name='user_views'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)