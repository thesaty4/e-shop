# Generated by Django 3.2.3 on 2021-07-27 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EshopApp', '0021_auto_20210727_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactusinfo',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 27, 4, 54, 6, 499039)),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='change_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 27, 4, 54, 6, 493046)),
        ),
    ]
