# Generated by Django 3.0.4 on 2020-05-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20200511_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(default='', max_length=10),
        ),
    ]
