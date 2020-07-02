from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, pagination, status,viewsets
from rest_framework.pagination import PageNumberPagination

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
import sys
from news.coc_news_util import *

sys.setrecursionlimit(1000000)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
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
    try:
        pass
        #profile = Profile.objects.get(id=1)
        # urls=collect_url(profile)
        execCollectArticleViaRss()
        execFetchRssArticleContentAndTranslateTitle()
        # collect_page(profile)
        # execTranslate()
    except:
        print(str(sys.exc_info()[0]))
        print(str(sys.exc_info()[1]))
        print(str(sys.exc_info()[2]))


def test(request):
    #execCollectArticleViaRss()
    #execFetchRssArticleContent()
    #execTranslate()
    # testResult=test_get_content_via_selector_and_link()
    # execFetchRssArticleContent()
    execFetchRssArticleContentAndTranslateTitle()
    # testResult=[]
    # articles=Article.getRssArticleWithoutContent()
    # for a in articles:
    #     testResult.append(a.toJSON())
    # return HttpResponse(json.dumps(testResult),content_type="application/json,charset=utf-8")

    testTranslateByGoogle()
    return HttpResponse('成功', content_type="application/json,charset=utf-8")

def testTranslateByGoogle():
    from news.coc_news_translate import translate_by_google
    result= translate_by_google('love')
    print(result)
# 获取文章正文


def execFetchRssArticleContentAndTranslateTitle():
    print(now()+u'--执行获取文章正文任务')
    fetchRssArticleContentAndTranslateTitle()

# 自动翻译


def execTranslate():
    print(now()+u'--执行自动翻译任务')
    articles = Article.objects.filter(process_status=1)[:5]
    if len(articles)<1 : 
        print('没有待翻译的文章')
        return
    for article in articles:
        # google
        # if notTranslatedWithEngine(article.guid, 'google'):
        #     zhArticle = translate_article_with_engine(article, 'google')
        #     zhArticle['type'] = "google"
        #     zhArticle['guid'] = article.guid
        #     a = Article_translation(**zhArticle)
        #     a.save()
        #     article.process_status=1
        #     article.save()
        # ali
        if notTranslatedWithEngine(article.guid, 'ali'):
            zhArticle=translate_article_with_engine(article,'ali')
            zhArticle['type']="ali"
            zhArticle['guid']=article.guid
            a=Article_translation(**zhArticle)
            a.save()
            article.process_status=2
            article.save()
        else:
            print(article.guid + '已经被ali翻译过了')
            

def notTranslatedWithEngine(guid, engine):
    result = []
    try:
        result = Article_translation.objects.get(guid=guid)
    except:
        return True
    else:
        if(result.content is not None):
            return False
        else :
            return True
# 自动收集rss数据


def execCollectArticleViaRss():
    print(now()+u'--执行rss收集任务')
    profiles = Profile.objects.filter(~Q(rss_url=''))
    articles = collect_article_via_rss(profiles)
    # logging.info(articles)
    temp = open('./temp.json', 'w+')
    temp.write(str(articles))
    temp.close()
    # 持久化
    for article in articles:
        title = article.title if ('title' in article) else ''
        from html import unescape
        title=unescape(title)
        try:
            aJson = {
                'guid': article.id if ('guid' in article) else (article['id'] if ('id' in article) else ''),
                'title': title,
                'summary': article.summary if ('summary' in article) else '',
                'description': article.description if ('description' in article) else '',
                'link': article.link if ('link' in article) else '',
                'pub_date': article.published if ('published' in article) else '',
                'source': article.source.title if ('source' in article) else '',
                'source_url': article.source.href if ('source' in article) else '',
                'media_content': article.media_content if ('media_content' in article) else '',
                'profile_name': article['profile_name'],
                'type': 'rss'
                # 'media_text':article.media_text
            }
        except:
            return u'解析失败:' + str(sys.exc_info()[0])
        else:
            if(len(Article.objects.filter(title=title)) == 0):
                a = Article(**aJson)
                a.save()
                logging.info('----新增文章:'+str(aJson))
    return articles






class ArticleTranslationViewSet(viewsets.ModelViewSet):
    queryset=Article_translation.objects.all()
    serializer_class=ArticleTranslationSerializer
    def list(self, request, *args, **kwargs):
        guid=None
        if(len(request.GET)>0):
            guid=request.GET.get('guid')
            engine=request.GET.get('engine')
            if engine is None:
                engine='ali'
        if guid is not None:     
            #没有的话先调用接口进行翻译
            article=Article.objects.get(guid=guid)
            if notTranslatedWithEngine(article.guid, engine):
                zhArticle=translate_article_with_engine(article,engine)
                zhArticle['type']=engine
                zhArticle['guid']=article.guid
                a=Article_translation(**zhArticle)
                a.save()
                article.process_status=2
                article.save()
            data = self.get_queryset().filter(guid__icontains=guid).filter(type=engine)
            if(len(data)>0):        
                serialized_data = self.get_serializer(data, many=True)
                return Response(serialized_data.data)        
        serialized_data = self.get_serializer({}, many=True)
        return Response(serialized_data)
             
    def get(self,request,*args,**kwargs):
        guid = request.GET('guid', None) # for GET requests
        #print(u'打印参数')
        #print(request.GET.urlencode())
        if guid is not None:
            data = self.get_queryset().filter(guid=guid)
            serialized_data = self.get_serializer(data, many=True)
            return Response(serialized_data.data)
        else :
            #print(u'打印参数2')
            return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        post_data=request.data.dict()
        post_data.pop('csrfmiddlewaretoken')
        article_translation=Article_translation(**post_data)
        return self.create(request,*args,**kwargs) 




# class ArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset=Article.objects.all().order_by('-update_time')
#     serializer_class=ArticleSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         post_data=request.data.dict()
#         post_data.pop('csrfmiddlewaretoken')
#         article_translation=Article_translation(**post_data)
#         return self.create(request,*args,**kwargs) 



class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-update_time')
    serializer_class = ArticleSerializer
    # filter_fields=('','')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_data = request.data.dict()
        post_data.pop('csrfmiddlewaretoken')
        article = Article(**post_data)
        return self.create(request, *args, **kwargs)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_fields = ('title', 'profile_name')


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
        # collect_url(profile)
        # collect_page(profile)
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

