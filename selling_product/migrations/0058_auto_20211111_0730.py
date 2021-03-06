# Generated by Django 3.2.3 on 2021-11-11 15:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('selling_product', '0057_auto_20211108_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 7, 30, 52, 131385), editable=False),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='order_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancel', 'Cancelled'), ('return', 'Return')], default='processing', max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertracking',
            name='status',
            field=models.CharField(choices=[('arrived', 'Arrived'), ('shipped', 'Shipped'), ('nearest hub', 'Reach Nearest Hub'), ('delivered', 'Finally Deliverd'), ('cancel', 'Cancelled')], default='arrived', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='add_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 7, 30, 52, 131385)),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='review_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 7, 30, 52, 131385)),
        ),
        migrations.AlterField(
            model_name='productsubscriber',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 7, 30, 52, 131385)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 7, 30, 52, 131385)),
        ),
        migrations.CreateModel(
            name='CheckoutItemOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selling_product.checkout')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
