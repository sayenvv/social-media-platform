"""
URL configuration for social_networking_media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views
from django.urls import include
from django.urls import path

from social_networking_app.views.authentication import LoginView
from social_networking_app.views.authentication import LogoutView
from social_networking_app.views.authentication import SignupView
from social_networking_app.views.social_accounts import FriendRequestView
from social_networking_app.views.social_accounts import ListUserView

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("login/", LoginView.as_view()),
                path("logout/", LogoutView.as_view(), name="logout"),
                path("sign-up/", SignupView.as_view()),
            ]
        ),
    ),
    path(
        "social/",
        include(
            [
                path("users/", ListUserView.as_view()),
                path(
                    "friend-requests/",
                    FriendRequestView.as_view(),
                    name="list-friend-request",
                ),
                path(
                    "friend-requests/send/",
                    FriendRequestView.as_view(),
                    name="send-friend-request",
                ),
                path(
                    "friend-requests/<int:pk>/",
                    FriendRequestView.as_view(),
                    name="accept-friend-request",
                ),
            ]
        ),
    ),
]
