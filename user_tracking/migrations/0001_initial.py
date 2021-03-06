# Generated by Django 3.2.3 on 2021-07-26 20:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('selling_product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=200)),
                ('query_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 331046))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClickSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 331046))),
                ('product_subcategories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selling_product.subcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClickProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 331046))),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selling_product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClickCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_click', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClickCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 331046))),
                ('product_categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selling_product.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
