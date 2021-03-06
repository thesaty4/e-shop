# Generated by Django 3.2.3 on 2021-11-05 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling_product', '0039_auto_20210828_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='tax',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 8, 11, 47, 775433)),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 8, 11, 47, 775433)),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 8, 11, 47, 775433)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 8, 11, 47, 775433)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 8, 11, 47, 775433)),
        ),
    ]
