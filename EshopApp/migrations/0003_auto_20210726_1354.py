# Generated by Django 3.2.3 on 2021-07-26 20:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EshopApp', '0002_auto_20210726_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us_info',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 54, 6, 994677)),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='change_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 54, 6, 979045)),
        ),
    ]
