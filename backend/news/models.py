from django.db import models
from news.BaseModel import BaseModel

#网站文章解析器
class Article_Selector_Website(BaseModel):
    website_url=models.CharField(max_length=200,default='')
    title_selector=models.CharField(max_length=200,default='',null=True,blank=True)
    author_selector=models.CharField(max_length=200,default='',null=True,blank=True)
    content_selector=models.CharField(max_length=200,default='',null=True,blank=True)
    
    def get_selector_by_url(url):
        result= Article_Selector_Website.objects.get(website_url__contains = url ).getDict() 
        return result


#翻译和处理后的文章
class Article_translation(models.Model):
    guid=models.CharField(max_length=200,default='')
    title=models.CharField(max_length=200,default='')
    summary=models.TextField(max_length=500000,default='')
    description=models.TextField(max_length=50000,default='')
    type=models.CharField(max_length=20,default='')
    update_time=models.TimeField(auto_now=True)
    content=models.TextField(max_length=5000000,default='')

#RSS文章
class Article(BaseModel):
    #id=models.CharField(max_length=200,default='',primary_key=True)
    title=models.CharField(max_length=200,default='')
    summary=models.TextField(max_length=500000,default='')
    description=models.TextField(max_length=50000,default='')
    link=models.CharField(max_length=1000,default='')
    pub_date=models.CharField(max_length=200,default='')
    source=models.CharField(max_length=200,default='')
    source_url=models.CharField(max_length=200,default='')
    guid=models.CharField(max_length=200,default='')
    media_content=models.CharField(max_length=2000,default='')
    media_text=models.TextField(max_length=50000,default='')
    profile_name=models.CharField(max_length=200,default='')
    update_time=models.TimeField(auto_now=True)
    process_status=models.IntegerField(default=0)
    content=models.TextField(max_length=5000000,default='')
    type=models.CharField(max_length=10,default='')

    def getRssArticleWithoutContent():
        aJson=[]
        articles=Article.objects.filter(type='rss',content='')
        for a in articles:
            aJson.append(a.getDict())
        return aJson


# 文章
class PageEN(models.Model):
    id=models.UUIDField(primary_key=True)
    link=models.CharField(max_length=200,default='')
    title=models.CharField(max_length=1000,default='')
    author=models.CharField(max_length=1000,default='')
    content=models.TextField(max_length=200,default='')
    profile=models.CharField(max_length=10,default='')

    class Meta:
        db_table = 'page_en'

    def __str__(self):
        return self.title

# 翻译后的中文文章
class PageCN(models.Model):
    title=models.CharField(max_length=1000,default='')
    author=models.CharField(max_length=1000,default='')
    content=models.TextField(max_length=200,default='')
    profile=models.CharField(max_length=10,default='')

    class Meta:
        db_table = 'page_cn'

    def __str__(self):
        return self.title


# 文章配置
class Profile(BaseModel):
    name=models.CharField(max_length=200,default='')
    title=models.CharField(max_length=200,default='')
    first_page=models.CharField(max_length=200,default='')
    url_selector=models.CharField(max_length=200,default='')
    title_selector=models.CharField(max_length=200,default='')
    author_selector=models.CharField(max_length=200,default='')
    content_selector=models.CharField(max_length=200,default='')
    rss_url=models.CharField(max_length=200,default='')

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.title