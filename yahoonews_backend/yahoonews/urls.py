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
from django.urls import path
from django.conf.urls import url
from . import view
import sys
from . import testdb
from . import msdb
from . import testGetArticle

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('hello/',view.hello),
    path('home/',view.home),
    path('getEnglishArticle/',view.getEnglishArticle),
    path('getChineseArticle/',view.getChineseArticle),
    path('saveProfile',msdb.saveProfile),
    path('queryProfile',msdb.queryProfile),
    path('deleteProfile',msdb.deleteProfile),
    path('resolveArticle',testGetArticle.resolveArticle),
    url(r'^testdb_save$', testdb.testdb_save),
    url(r'^testdb_get$', testdb.testdb_get),
    url(r'^testdb_update$', testdb.testdb_update),
    url(r'^testdb_delete$', testdb.testdb_delete),
    #url(r'^$',view.hello)
]
