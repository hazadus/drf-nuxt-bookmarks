from django.urls import path

from .views import LoggedInUserDetailView, UserUpdateView

urlpatterns = [
    path("user/details/", LoggedInUserDetailView.as_view()),
    path("user/<int:pk>/", UserUpdateView.as_view()),
]
