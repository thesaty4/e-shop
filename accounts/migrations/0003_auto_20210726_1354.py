# Generated by Django 3.2.3 on 2021-07-26 20:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210726_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 7, 26, 13, 54, 7, 391331), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='reg_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 54, 7, 391331)),
        ),
    ]
