# Generated by Django 3.2.3 on 2021-07-27 06:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EshopApp', '0014_auto_20210726_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='titleoffaq',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='EshopApp.siteinfo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactusinfo',
            name='at_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 23, 49, 10, 534993)),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='change_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 23, 49, 10, 522998)),
        ),
    ]
