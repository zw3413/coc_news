# Generated by Django 3.0.4 on 2020-05-13 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20200513_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_selector_website',
            name='author_selector',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='article_selector_website',
            name='content_selector',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='article_selector_website',
            name='title_selector',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
