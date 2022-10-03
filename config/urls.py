"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from cards.views import *
from config import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf_auth/', include('rest_framework.urls')),
    path('api/v1/card/', CardAPIList.as_view(), name="user_cards"),
    path('api/v1/card/<int:pk>/', CardAPIUpdate.as_view(), name="update_cards"),
    path('api/v1/carddelete/<int:pk>/', CardAPIDestroy.as_view(), name="delete_card"),
    path('api/v1/category/', CategoryAPIList.as_view(), name="user_category"),
    path('api/v1/category/<int:pk>/', CategoryAPIUpdate.as_view(), name="update_category"),
    path('api/v1/categorydelete/<int:pk>/', CategoryAPIDestroy.as_view(), name="delete_category"),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

