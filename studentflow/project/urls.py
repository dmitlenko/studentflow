from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('studentflow.base.urls')),
    path('chat/', include('studentflow.chat.urls')),
    path('api/', include('studentflow.api.urls'))
]
