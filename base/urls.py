from django.urls import path
from . import views

# url patterns for the base app
urlpatterns = [
    path('', views.MainView.as_view()),
    
]
