# Generated by Django 3.2.3 on 2021-11-06 16:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_auto_20211106_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 9, 35, 0, 833563)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 9, 35, 0, 833563)),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='reply_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 9, 35, 0, 833563)),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 9, 35, 0, 833563)),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 6, 9, 35, 0, 833563)),
        ),
    ]
