# Generated by Django 3.2.3 on 2021-11-08 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling_product', '0049_auto_20211108_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 8, 8, 57, 903603), editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 8, 8, 57, 903603)),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 8, 8, 57, 903603)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 8, 8, 57, 903603)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 8, 8, 57, 903603)),
        ),
    ]
