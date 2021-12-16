# Generated by Django 3.2.3 on 2021-08-28 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling_product', '0038_auto_20210828_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 28, 4, 59, 55, 451756)),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 28, 4, 59, 55, 451756)),
        ),
        migrations.AlterField(
            model_name='product',
            name='offer_end',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Offer End YYYY/MM/DD'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 28, 4, 59, 55, 451756)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 28, 4, 59, 55, 467396)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 28, 4, 59, 55, 467396)),
        ),
    ]
