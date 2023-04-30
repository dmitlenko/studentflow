from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# url patterns for the base app
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('auth/signup', views.SignupView.as_view(), name='signup'),

    path('post/create', views.PostCreateView.as_view(), name='create_post'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='detail_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)