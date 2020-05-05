from django.db import models


#RSS文章
class Article(models.Model):
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
class Profile(models.Model):
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