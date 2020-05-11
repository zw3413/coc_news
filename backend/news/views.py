from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, pagination, status
from lxml import etree
import requests
from news.coc_news import *
from django.db.models import Q
from django.http import HttpResponse
from news.models import *
from news.serializers import *
import json
import logging
import time

headers= {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'max-age=0',
'cookie': 'B=17s48ohf7343b&b=3&s=vi; A3=d=AQABBGuQcV4CENeFySADe2JywU_yiMSI8BMFEgEBAQHhcl57XgAAAAAA_SMAAAcIa5BxXsSI8BM&S=AQAAAhmGLOk-qd7Dcz8wMHYyjHU; APID=UPc0d0c016-68ca-11ea-a723-06c362194baa; A1=d=AQABBGuQcV4CENeFySADe2JywU_yiMSI8BMFEgEBAQHhcl57XgAAAAAA_SMAAAcIa5BxXsSI8BM&S=AQAAAhmGLOk-qd7Dcz8wMHYyjHU; ucs=lbit=1584951070; A1S=d=AQABBGuQcV4CENeFySADe2JywU_yiMSI8BMFEgEBAQHhcl57XgAAAAAA_SMAAAcIa5BxXsSI8BM&S=AQAAAhmGLOk-qd7Dcz8wMHYyjHU&j=WORLD; APIDTS=1585193822; cmp=t=1585193915&j=0; GUCS=ARBij1S1; GUC=AQEBAQFecuFee0IaBgO4',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1'}


# 定时任务
def auto_task():
    print('auto task triggered')
    #profile = Profile.objects.get(id=1)
    #urls=collect_url(profile)
    execCollectArticleViaRss()
    #collect_page(profile)
    #execTranslate()
    pass

# 自动翻译
def execTranslate():
    print(now()+u'--执行自动翻译任务')
    articles=Article.objects.filter(process_status = 0)
    for article in articles:
        cnArticleJson={}
        for key in article.keySet():
            if(key == 'title' or key == 'summary'):
                enText=article[key]
                cnTextJson=translate_english_to_Chinese(enText)
                cnArticleJson[key]=cnTextJson
        a=Article_translation(**cnArticleJson)
        a.save()        

# 自动收集rss数据
def execCollectArticleViaRss():
    print(now()+u'--执行rss收集任务')
    profiles=Profile.objects.filter(~Q(rss_url =''))
    articles=collect_article_via_rss(profiles)
    #logging.info(articles)
    temp = open('./temp.json', 'w+')
    temp.write(str(articles))
    temp.close()
    # 持久化
    for article in articles:
        aJson={
            'guid':article.id if article.has_key('guid') else (article.id if article.has_key('id') else ''),
            'title':article.title if article.has_key('title') else '',
            'summary':article.summary if article.has_key('summary') else '',
            'description':article.description if article.has_key('description') else '',
            'link':article.link if article.has_key('link') else '',
            'pub_date':article.published if article.has_key('published') else '',
            'source':article.source.title if article.has_key('source') else '',
            'source_url':article.source.href if article.has_key('source') else '',
            'media_content':article.media_content if article.has_key('media_content') else '',
            'profile_name': article.profile_name
            #'media_text':article.media_text
        }
        title=article.title
        #print(len(Article.objects.filter(title = title)))
        if(len(Article.objects.filter(title = title))==0):
            a=Article(**aJson)
            a.save()
            print(now()+'----新增文章:'+str(aJson))
    return articles
def now():
    return time.asctime(time.localtime(time.time()))

def test(request):
    return HttpResponse(json.dumps(execCollectArticleViaRss()),content_type="application/json,charset=utf-8")


class ArticleList(generics.ListCreateAPIView):
    queryset=Article.objects.all().order_by('-update_time')
    serializer_class=ArticleSerializer
    #filter_fields=('','')
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        post_data=request.data.dict()
        post_data.pop('csrfmiddlewaretoken')
        article=Article(**post_data)    
        return self.create(request,*args,**kwargs)

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_fields = ('title','profile_name')


# # 数据采集
# def collect_url(profile):
#     first_page = 'https://news.yahoo.com/world/'
#     url_selector='#Main ul'
#     html_doc = requests.get(first_page, headers=headers).text
#     tree = etree.HTML(html_doc)
#     print(tree.xpath('//*[@id="item-0"]/ul'))

# def collect_page(profile):
#     pass

class ProfileList(generics.ListCreateAPIView):
    """
    get: 获取已有配置列表
    post: 提交新建配置列表
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_fields = ('name', 'title')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_data = request.data.dict()
        post_data.pop('csrfmiddlewaretoken')
        profile = Profile(**post_data)
        #collect_url(profile)
        #collect_page(profile)
        return self.create(request, *args, **kwargs)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_fields = ('name', 'title')


# Page EN
class PageENList(generics.ListCreateAPIView):
    queryset = PageEN.objects.all()
    serializer_class = PageENSerializer

class PageENDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageEN.objects.all()
    serializer_class = PageENSerializer


# Page CN
class PageCNList(generics.ListCreateAPIView):
    queryset = PageCN.objects.all()
    serializer_class = PageCNSerializer

class PageCNDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageCN.objects.all()
    serializer_class = PageCNSerializer


