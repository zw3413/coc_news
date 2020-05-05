"""yahoonews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path

from news.views import *
from news.serializers import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/',test),
    path('profile/', ProfileList.as_view(), name='profile_list'),
    re_path('profile/(?P<pk>[0-9]+)/', ProfileDetail.as_view(), name='profile_detail'),
    path('pageen/', PageENList.as_view(), name='pageen_list'),
    re_path('pageen/(?P<pk>[0-9]+)/', PageENList.as_view(), name='pageen_detail'),
    path('pagecn/', PageCNList.as_view(), name='pagecn_list'),
    re_path('pagecn/(?P<pk>[0-9]+)/', PageCNDetail.as_view(), name='pagecn_detail'),
    path('article/', ArticleList.as_view(), name='article_list'),
    re_path('article/(?P<pk>[0-9]+)/', ArticleDetail.as_view(), name='article_detail'),
]