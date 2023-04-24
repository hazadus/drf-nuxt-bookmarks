from django.urls import path

from .views import download_start_from_web

urlpatterns = [
    path("downloads/start/", download_start_from_web),
]
