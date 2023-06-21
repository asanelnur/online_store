from django.urls import path, include

urlpatterns = [
    path('', include('src.urls.v1')),
    path('', include('users.urls.v1')),
]
