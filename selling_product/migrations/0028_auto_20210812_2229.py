# Generated by Django 3.2.3 on 2021-08-13 05:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling_product', '0027_auto_20210811_0907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewvote',
            old_name='is_up_vote',
            new_name='is_like',
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 29, 34, 889882)),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 29, 34, 888883)),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 29, 34, 889882)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 29, 34, 891880)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 22, 29, 34, 890881)),
        ),
    ]
