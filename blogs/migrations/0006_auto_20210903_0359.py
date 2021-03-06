# Generated by Django 3.2.3 on 2021-09-03 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20210903_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='blogs/audio/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogs/images/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='video',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='reply_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
        migrations.AlterField(
            model_name='subcommentvote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 3, 3, 59, 45, 899357)),
        ),
    ]
