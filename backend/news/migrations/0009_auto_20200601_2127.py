# Generated by Django 2.2 on 2020-06-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20200601_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
