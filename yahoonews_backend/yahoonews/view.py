from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
import json
from . import bs4util

def hello(request):
    context={}
    context['hello']="Hello World!"
    context['condition']=True
    #context['a']=2
    context['b']=1
    context['list']=['john','lily','david','kitty']
    return render(request,'hello.html',context)
 

def home(request):
    context={}
    global articleCache,cnArticleCache,currentArticleUrl
    #articleCache={}
    #cnArticleCache={}
    #currentArticleUrl=''
    urls=bs4util.getArticleUrl_YahooNews()
    urlObjs=[]
    for u in urls:
        title= u.split('/')[3].split('.')[0]
        url={
            'url':u,
            'title':title
        }
        urlObjs.append(url)
    context['urls']=urlObjs
    return render(request,'home.html',context)

articleCache={}
cnArticleCache={}
currentArticleUrl=''
def getEnglishArticle(request):
    url=request.GET['url']
    global currentArticleUrl
    currentArticleUrl=url
    if url in articleCache.keys():
        return JsonResponse({
            'code':'200',
            'data':json.dumps(articleCache[url]),
            'msg':'success'
        })
    else:
        englishArticle= bs4util.getArticle_YahooNews(url)
        articleCache[url]=englishArticle
        return JsonResponse({
            'code':'200',
            'data':json.dumps(englishArticle),
            'msg':'success'
        })
def getChineseArticle(request):
    if currentArticleUrl in cnArticleCache.keys():
        return JsonResponse({
            'code':'200',
            'data':json.dumps(cnArticleCache[currentArticleUrl]),
            'msg':'success'
        })
    else:
        currentArticle=articleCache[currentArticleUrl]
        cnArticle={}
        bs4util.translateArticle(currentArticle,cnArticle)
        #print(cnArticle)
        #cnArticle=cnArticle[currentArticleUrl]
        cnArticleCache[currentArticleUrl]=cnArticle
        return JsonResponse({
            'code':'200',
            'data':json.dumps(cnArticle),
            'msg':'success'
        })