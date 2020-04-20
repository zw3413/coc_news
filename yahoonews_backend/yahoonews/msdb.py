# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.http import JsonResponse
from TestModel.models import Profile
from django.core import serializers
import json
def deleteProfile(request):
    try:
        name=request.GET['name']
        p=Profile.objects.filter(name=name)
        p.delete()
        return JsonResponse({
            'code':'200',
            'data':'',
            'msg':'success'
        })
    except Exception as err:
        return JsonResponse({
            'code':'500',
            'data':"{0}".format(err),
            'msg':'fail'
        })

def saveProfile(request):
    try:
        name=request.GET['name']
        p=Profile.objects.filter(name=name)
        if len(p)>0:
            p.delete()
        profile=Profile(name=name)    
        profile.title=request.GET['title']
        profile.first_page=request.GET['firstPage']
        profile.url_selector=request.GET['urlSelector']
        profile.title_selector=request.GET['titleSelector']
        profile.author_selector=request.GET['authorSelector']
        profile.content_selector=request.GET['contentSelector']
        profile.save()
        return JsonResponse({
            'code':'200',
            'data':'',
            'msg':'success'
        })
    except Exception as err:
        return JsonResponse({
            'code':'500',
            'data':"{0}".format(err),
            'msg':'fail'
        })    
    

def queryProfile(request):
    profiles=Profile.objects.all()
    return JsonResponse({
        'code':'200',
        'data':serializers.serialize('json',profiles),
        'msg':'success'
    })