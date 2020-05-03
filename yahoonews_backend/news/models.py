from django.db import models

#自动获取的url列表
class url(models.Model):
    url=models.CharField(max_length=1000)
    updatetime=models.TimeField
    profile_id=models.CharField(max_length=200)

# 文章
class PageEN(models.Model):
    title=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    content=models.TextField(max_length=200)
    profile=models.CharField(max_length=10)

    class Meta:
        db_table = 'page_en'

    def __str__(self):
        return self.title

# 翻译后的中文文章
class PageCN(models.Model):
    title=models.CharField(max_length=1000)
    author=models.CharField(max_length=1000)
    content=models.TextField(max_length=200)
    profile=models.CharField(max_length=10)

    class Meta:
        db_table = 'page_cn'

    def __str__(self):
        return self.title


# 文章配置
class Profile(models.Model):
    id=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    title=models.CharField(max_length=200,default='')
    first_page=models.CharField(max_length=200,default='')
    url_selector=models.CharField(max_length=200,default='')
    title_selector=models.CharField(max_length=200,default='')
    author_selector=models.CharField(max_length=200,default='')
    content_selector=models.CharField(max_length=200,default='')

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.title