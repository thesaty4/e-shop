# Generated by Django 3.2.3 on 2021-11-06 07:35

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_auto_20210908_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 0, 35, 39, 676011)),
        ),
        migrations.AlterField(
            model_name='blog',
            name='discription',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 0, 35, 39, 677011)),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='reply_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 0, 35, 39, 678010)),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 0, 35, 39, 678010)),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 0, 35, 39, 677011)),
        ),
    ]
