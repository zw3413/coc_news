# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from TestModel.models import Profile
from TestModel.models import Page
from django.core import serializers
import json
import requests
from bs4 import BeautifulSoup

def resolveArticle(request):
    profiles=Profile.objects.all()
    for profile in profiles:
        print('name:'+profile.name)
        print('title:'+profile.title)
        print('first_page:'+profile.first_page)
        print('url_selector:'+profile.url_selector)
        print('author_selector:'+profile.author_selector)
        print('content_selector:'+profile.content_selector)
        result=ra(profile)
    return JsonResponse({
        'code':'',
        'data':result,
        'msg':'success'
    })

def ra(profile):
    return getUrlList(profile.first_page,profile.url_selector)

def getUrlList(firstPageUrl,urlSelector):
    resp=requests.get(firstPageUrl)
    resp.encoding="utf-8"
    soup=BeautifulSoup(resp.text,'html.parser')
    return soup.prettify()
