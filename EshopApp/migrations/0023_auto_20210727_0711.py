# Generated by Django 3.2.3 on 2021-07-27 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EshopApp', '0022_auto_20210727_0454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='site',
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 27, 7, 11, 21, 616613)),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='change_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 27, 7, 11, 21, 612617)),
        ),
    ]
