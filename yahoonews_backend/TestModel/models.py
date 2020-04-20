from django.db import models

# Create your models here.
# 类名Test代表数据库名 且继承了models.Model
class Test(models.Model):
    name = models.CharField(max_length=20)

class Profile(models.Model):
    name=models.CharField(max_length=200)
    title=models.CharField(max_length=200,default='')
    first_page=models.CharField(max_length=200,default='')
    url_selector=models.CharField(max_length=200,default='')
    title_selector=models.CharField(max_length=200,default='')
    author_selector=models.CharField(max_length=200,default='')
    content_selector=models.CharField(max_length=200,default='')

class Page(models.Model):
    title=models.CharField(max_length=200)
    author_selector=models.CharField(max_length=200)
    content_selector=models.CharField(max_length=200)
    profile_name=models.CharField(max_length=200)