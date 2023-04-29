from django.urls import path
from . import views

# url patterns for the base app
urlpatterns = [
    path('', views.IndexView.as_view(), name='index_view'),
    path('auth/login', views.LoginView.as_view(), name='login_view'),
    path('auth/logout', views.logout_view, name='logout_view'),
    path('auth/register', views.RegistrationView.as_view(), name='registration_view')
]
