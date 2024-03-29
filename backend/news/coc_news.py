# -*- coding: UTF-8 -*-
from lxml import etree
import requests
from bs4 import BeautifulSoup
import codecs
import feedparser
import json
import logging
import sys
import traceback
from news.coc_news_translate import *
from news.coc_news_util import *

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

def translate_article_with_engine(enArticle,engine):
    keyToTranslate=['title','summary','content']
    zhArticle={}
    fields=enArticle._meta.fields
    if engine=='google':
        for f in fields:
            if f.name in keyToTranslate:
                zhArticle[f.name]=translate_by_google(enArticle.__getattribute__(f.name) )
    elif engine == 'ali':
        for f in fields:
            if f.name in keyToTranslate:
                zhArticle[f.name]=translate_by_ali(enArticle.__getattribute__(f.name) )
    elif engine == 'youdao':
        for f in fields:
            if f.name in keyToTranslate:
                zhArticle[f.name]=translate_by_youdao(enArticle.__getattribute__(f.name) )
    elif engine == 'bing':            
        for f in fields:
            if f.name in keyToTranslate:
                zhArticle[f.name]=translate_by_bing(enArticle.__getattribute__(f.name) )
    return zhArticle

def fetchRssArticleContentAndTranslateTitle():
    from news.models import Article
    from urllib.parse import urlparse
    #获取尚未获取正文的RSS文章列表
    articles=Article.getRssArticleWithoutContent()
    for article in articles:
        #只处理有link字段的article,link字段指向正文页面，在正文页面提取文章内容
        if(('link' in article) and  ( len(article['link'])>0 )):
            link=article['link']

            selector=get_selector_via_source(article['source_url'])
            if selector==None or len(selector)==0:
                res=urlparse(link)
                selector=get_selector_via_source(res.scheme+'://'+res.netloc)
            if selector==None or len(selector)==0:
                selector=get_selector_via_profile(article['profile_name'])
            if selector==None or len(selector)==0:
                return                     

            content=get_article_content_via_selector_and_link(selector,link)
            if content != None and len(content)!=0:
                 #翻译文档标题
                title=article['title']
                from news.coc_news_translate import translate_by_google 
                # zhTitle=translate_by_google(title)
                zhTitle=translate_by_ali(title)
                from html import unescape
                zhTitle=unescape(zhTitle)
                article['zh_title']=zhTitle
                #过滤content
                try:
                    def cleanContent(content):
                        import re
                        pattern=r'<a.*?>|</a>|<ul.*>.*</ul>|<button.*?/button>'
                        cleanedContent=re.sub(pattern,'',content)
                        p1='data-src'
                        cleanedContent=re.sub(p1,'src',cleanedContent)
                        return cleanedContent
                    article['content']=cleanContent(content)
                    article['process_status']=1
                    a=Article(**article)
                    a.save()
                    print(now()+u"--获取和保存文章正文成功"+article['title'])
                except:
                    exc_type, exc_value, exc_obj = sys.exc_info()
                    traceback.print_tb(exc_obj)
                    print(now()+u'--获取和保存文章正文失败'+article['title'])
             
                
       
        

# 解析url
def collect_url(profile,mode="css"):
    if(mode == 'css'):
        collect_url_via_css(profile)
    elif (mode == 'xml'):
        collect_url_via_xml(profile)
    
def collect_url_via_xml(profile):   
    html_doc = requests.get(profile['first_page'], headers=headers).text
    tree = etree.HTML(html_doc)
    print(tree)
    print(tree.xpath('//*[@id="Main"] ul'))

def collect_url_via_css(profile):
    res=requests.get(profile['first_page'],headers=headers)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup.prettify())
    urls=[]
    for ele in soup.select(profile['url_selector']):
        while (ele.name!='a') :
            ele=ele.find('a')
        if(ele.name=='a'):
            #print(ele)
            #print(ele.name)
            u = ele['href']
            urls.append(u)
    return urls

def collect_article_via_rss(profiles):
    articles=[]
    for profile in profiles:
        profile=profile.getDict()
        logging.info(profile)
        url = profile['rss_url']
        try:
            res = requests.get(url, headers=headers,timeout=5)
        except:
            logging.info('请求超时：'+ url)
        else:
            res.encoding = 'utf-8'
            #解析返回的feed
            feed=feedparser.parse(res.text)    
            
            #print(profile.name)
            #print(profile.rss_url)
            #print(type(profile))
            for entry in feed.entries:
                #为所有feed添加profile name
                entry['profile_name']=profile['name']
            articles.append(entry)    
    return articles

# 根据文章链接和CSS选择器来获取文章内容
def get_article_content_via_selector_and_link(selector,link):
    response=requests.get(link,headers=headers,timeout=10)
    response.encoding='UTF-8'
    soup=BeautifulSoup(response.text,'html.parser')
    #print(soup.prettify())
    content=''
    result = ''
    if('content_selector' in selector):
        print('采集正文:'+link)
        content=soup.select(selector['content_selector'])
    else:
        print('没有检测到正文选择器:'+link)  

    if(str(type(content))== "<class 'bs4.element.ResultSet'>" or str(type(content))=="<class 'list'>"):
        for c in content:
            result = result + str(c)
    else:
        result=content    
    return result
    
#根据文章来源查询CSS选择器    
def get_selector_via_source(url):
    from news.models import Article_Selector_Website
    try:
        return Article_Selector_Website.get_selector_by_url(url)
    except:
        return None

def get_selector_via_profile(profile_name):
    from news.models import Profile
    try:
        return Profile.get_content_selector_by_profile_name(profile_name)
    except:
        return None 

def translate_english_to_Chinese(enText):
    #翻译引擎一：阿里翻译API
    
    pass

def test_collect_article_via_rss():
    profile={
        'first_page' : 'https://news.yahoo.com/world/',
        'url_selector' :'#Main li',
        'rss_url':'https://www.yahoo.com/news/rss'
    }
    #collect_url(profile)
    a=collect_article_via_rss(profile)
    print(a)

def test_get_content_via_selector_and_link():
    link='https://www.politico.com/news/2020/05/04/mccarthy-mcconnell-testing-coronavirus-233984'
    selector = get_selector_via_source('https://www.politico.com/')
    content=get_article_content_via_selector_and_link(selector,link)
    print(content)
    return content

if __name__ == "__main__":
    #test_collect_article_via_rss()
    #test_get_content_via_profile_and_link()
    #test_get_selector_via_source()
    pass