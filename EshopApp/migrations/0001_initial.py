# Generated by Django 3.2.3 on 2021-07-26 20:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('discription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='FaqInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('discription', models.TextField(max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='site_info_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_lable', models.CharField(max_length=100)),
                ('image_path', models.ImageField(upload_to='site_config_img/images/')),
                ('is_blog', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=20)),
                ('mobile', models.CharField(help_text='Enter Mobile Number in International Format +', max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField(max_length=500)),
                ('working_time', models.CharField(max_length=100)),
                ('google_map_api', models.CharField(help_text='Find API KEY At : https://console.cloud.google.com/google/maps-apis/credentials', max_length=1000)),
                ('latitude', models.CharField(help_text='Go to https://www.google.com/maps/ and right click to copy Latitude & Longitude', max_length=100)),
                ('longitude', models.CharField(help_text='Go to https://www.google.com/maps/ and right click to copy Latitude & Longitude', max_length=100)),
                ('facebook_id', models.CharField(help_text='https://facebook.com/(USER_ID)', max_length=100)),
                ('instagram_id', models.CharField(help_text='https://instagram.com/(USER_ID)', max_length=100)),
                ('twitter_id', models.CharField(help_text='https://twitter.com/(USER_ID)', max_length=100)),
                ('youtube_id', models.CharField(help_text='https://youtube.com/(USER_ID)', max_length=100)),
                ('linkedin_id', models.CharField(help_text='https://linkedin.com/(USER_ID)', max_length=100)),
                ('logo', models.ImageField(upload_to='site_config_img/logo/', verbose_name='Logo 85x27')),
                ('preloader', models.ImageField(upload_to='site_config_img/preloader/', verbose_name='Preloader 50x50')),
                ('loader', models.ImageField(upload_to='site_config_img/loader/', verbose_name='Loader 32x32')),
                ('fav_icon', models.ImageField(upload_to='site_config_img/favi_icon/', verbose_name='Favicon 32x32 Size')),
                ('copyright', models.CharField(max_length=50)),
                ('site_url_domain', models.URLField()),
                ('change_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 61100))),
            ],
        ),
        migrations.CreateModel(
            name='SiteOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_title', models.CharField(max_length=100)),
                ('offer_name', models.CharField(max_length=100)),
                ('offer_end', models.CharField(max_length=100, verbose_name='Offer End YYYY/MM/DD')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='Select Gender', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SiteFaq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='Write Question', max_length=150)),
                ('answer', models.TextField(help_text='Please write suitable answer..', max_length=500)),
                ('Faq_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EshopApp.faqinfo')),
            ],
        ),
        migrations.CreateModel(
            name='site_info_img_content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_title', models.CharField(max_length=100)),
                ('offer', models.CharField(max_length=100)),
                ('offer_desc', models.CharField(max_length=100)),
                ('offer_start_at', models.IntegerField()),
                ('site_info_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EshopApp.site_info_img')),
            ],
        ),
        migrations.AddField(
            model_name='site_info_img',
            name='site_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EshopApp.siteinfo'),
        ),
        migrations.CreateModel(
            name='contact_us_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=500)),
                ('at_date_time', models.DateTimeField(default=datetime.datetime(2021, 7, 26, 13, 51, 20, 63124))),
                ('contact_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EshopApp.contactus')),
            ],
        ),
    ]
