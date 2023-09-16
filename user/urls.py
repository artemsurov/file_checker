from django.urls import include

from django.urls import path

urlpatterns = [
    path('', include('djoser.urls.base')),
    path('', include('djoser.urls.authtoken')),
]
