# Generated by Django 3.2.3 on 2021-11-08 15:26

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('selling_product', '0046_auto_20211108_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=100)),
                ('langitude', models.CharField(max_length=100)),
                ('pin_code', models.IntegerField()),
                ('leave_note', tinymce.models.HTMLField()),
                ('arrival_time', models.TimeField(default=datetime.time)),
                ('arrival_date', models.DateField(default=datetime.date)),
                ('leaved_time', models.TimeField(default=datetime.time)),
                ('leaved_date', models.DateField(default=datetime.date)),
            ],
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 7, 26, 17, 535922), editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 7, 26, 17, 535922)),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 7, 26, 17, 551543)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 7, 26, 17, 551543)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 8, 7, 26, 17, 551543)),
        ),
        migrations.DeleteModel(
            name='order_tracking',
        ),
        migrations.AddField(
            model_name='ordertracking',
            name='tracking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selling_product.checkout'),
        ),
    ]
