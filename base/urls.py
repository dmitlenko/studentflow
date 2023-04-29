from django.urls import path
from . import views

# url patterns for the base app
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('auth/signup', views.SignupView.as_view(), name='signup')
]
