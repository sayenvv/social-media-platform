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
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema = get_schema_view(
    openapi.Info(title="API", default_version="1.0.0", description="fdsfsd"),
    public=True,
)


urlpatterns = [
    # path to rest authentication
    path("rest/", include("rest_framework.urls", namespace="rest_framework")),
    # path to django admin panel
    path("admin/", admin.site.urls),
    # path to swagger : API documentation
    path("api_docs/", schema.with_ui("swagger", cache_timeout=0), name="swagger"),
    # path to our social media apis
    path(
        "api/v0/", include("social_networking_app.urls")
    ),  # Add '.urls' to the included app's URLconf
]
