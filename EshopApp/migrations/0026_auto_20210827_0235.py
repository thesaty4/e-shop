# Generated by Django 3.2.3 on 2021-08-27 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EshopApp', '0025_auto_20210827_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopbydealsimage',
            name='lable',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 27, 2, 35, 27, 523653)),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='change_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 27, 2, 35, 27, 502776)),
        ),
    ]
