# -*- coding: UTF-8 -*-
from lxml import etree
import requests
from bs4 import BeautifulSoup
import codecs
import feedparser
import json
import logging

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
        logging.info(profile)
        url = profile.rss_url
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        #解析返回的feed
        feed=feedparser.parse(res.text)    
        
        print(profile.name)
        for entry in feed.entries:
            #为所有feed添加profile name
            entry['profile_name']=profile.name
            #获取其文章正文
            if(entry.has_key('link') and len(entry['link'] )>0):
                
                 # 根据profile获取选择器
                if(profile.has_key('rss_url')):
                    #rss类型的去Article_Selector_Website
                    selector=get_selector_via_source(entry.source.href)

                content=get_article_content_via_profile_and_link(profile,entry['link'])
                entry['content']=content
            articles.append(entry)
    return articles
def get_article_content_via_profile_and_link(selector,link):
    response=requests.get(link,headers=header)
    response.encoding='UTF-8'
    soup=BeautifuleSoup(response.text,'html.parser')
    print(soup.prettify())
    if(profile.has_key('content_selector')):
        if selector.has_key("content_selector"):    
            print('开始采集正文')
            content_selector= selector.content_selector
            content=soup.select(profile.content_selector)
        else:
            print('没有检测到正文选择器')
            content=''    
        print(content)
    pass
def get_selector_via_source(url):
    selector=Article_Selector_Website.objects.get(website_url=url)
    return selector
    pass
def test_get_selector_via_source():
    url=''
    selector=get_selector_via_source(url)
    print(json.dumps(selector))

def test_get_content_via_profile_and_link():
    profile={
        'content_selector':''
    }
    link='https://www.politico.com/news/2020/05/04/mccarthy-mcconnell-testing-coronavirus-233984'
    content=get_article_content_via_profile_and_link(profile,link)
    return content
    pass

def translate_english_to_Chinese():
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

if __name__ == "__main__":
    #test_collect_article_via_rss()
    test_get_content_via_profile_and_link()
    pass