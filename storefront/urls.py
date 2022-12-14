"""storefront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

""" Edit admin header title and index header """
admin.site.site_header = "Storefront Administration"
admin.site.index_title = "Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("core.urls")),
    # Add djoser authentication library to project urls
    path("auth/", include("djoser.urls")),
    # Use djoser with jwt as a backend authentication
    path("auth/", include("djoser.urls.jwt")),
    path("playground/", include("playground.urls")),
    path("store/", include("store.urls")),

]

if settings.DEBUG:
    # Set media url and root path for development environment
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
