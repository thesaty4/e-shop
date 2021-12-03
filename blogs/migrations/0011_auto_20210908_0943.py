# Generated by Django 3.2.3 on 2021-09-08 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_auto_20210908_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 9, 43, 40, 646574)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 9, 43, 40, 646574)),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='reply_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 9, 43, 40, 646574)),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 9, 43, 40, 646574)),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 8, 9, 43, 40, 646574)),
        ),
        migrations.DeleteModel(
            name='SubCommentVote',
        ),
    ]
