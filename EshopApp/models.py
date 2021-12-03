from typing import Sequence
from django.db import models
import datetime
from django.db.models.deletion import CASCADE
from tinymce.models import HTMLField
from django.contrib import admin
from django.utils.html import format_html
# Create your models here.
class SiteInfo(models.Model):
    shop_name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20,help_text="Enter Mobile Number in International Format +")
    email = models.EmailField()
    address = models.TextField(max_length=500)
    working_time = models.CharField(max_length=100)
    google_map_api = models.CharField(max_length=1000, help_text="Find API KEY At : https://console.cloud.google.com/google/maps-apis/credentials")
    latitude = models.CharField(max_length=100 , help_text="Go to https://www.google.com/maps/ and right click to copy Latitude & Longitude")
    longitude = models.CharField(max_length=100, help_text="Go to https://www.google.com/maps/ and right click to copy Latitude & Longitude")
    facebook_id = models.CharField(help_text="https://facebook.com/(USER_ID)",max_length=100)
    instagram_id = models.CharField(help_text="https://instagram.com/(USER_ID)",max_length=100)
    twitter_id = models.CharField(help_text="https://twitter.com/(USER_ID)",max_length=100)
    youtube_id = models.CharField(help_text="https://youtube.com/(USER_ID)",max_length=100)
    linkedin_id = models.CharField(help_text="https://linkedin.com/(USER_ID)",max_length=100)
    logo = models.ImageField(upload_to="site_config_img/logo/",verbose_name="Logo 85x27")
    preloader = models.ImageField(upload_to="site_config_img/preloader/",verbose_name="Preloader 50x50")
    loader = models.ImageField(upload_to="site_config_img/loader/",verbose_name="Loader 32x32")
    fav_icon = models.ImageField(upload_to='site_config_img/favi_icon/',verbose_name="Favicon 32x32 Size")
    copyright = models.CharField(max_length=50)
    site_url_domain = models.URLField()
    change_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.shop_name
    @admin.display
    def site_logo(self):
        return format_html('<img src="/media/%s" width="85" height="27" />'%(self.logo))
    class Meta:
        verbose_name_plural ="SITE info"

class ShopByDealsImage(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    lable=models.IntegerField(default=1)
    image = models.ImageField(upload_to='site_config_img/shop_by_deals/')
    def __str__(self):
        return "Deals Images of "+str(self.site)+" site"

class Slider(models.Model):
    site_info = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    offer_title = models.CharField(max_length=100,help_text="Write title of offer. Ex- Latest Update Brand")
    offer = models.CharField(max_length=100,help_text="What is your offer. Ex- 40%/ of on Electronic ")
    offer_desc = models.CharField(max_length=100,help_text="Discribe the offer for best understating.")
    offer_start_at = models.FloatField(help_text="Write offer stating price")
    resolution = models.CharField(max_length=50,default="1920x900")
    image = models.ImageField(upload_to="site_config_img/images/",help_text="recomended resolution - 1920x900")
    is_blog = models.BooleanField(default=False)
    def __str__(self):
        return "Slider - "+str(self.resolution)
    class Meta:
        verbose_name_plural ="Slider"

class BackgroundBanner(models.Model):
    site_info = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    resolution = models.CharField(max_length=50,default="1920x750",help_text="1920x750, recomended resolution")
    image = models.ImageField(upload_to="site_config_img/images/",help_text="recomended resolution - 1920x900")

    def __str__(self):
        return "Background Banner ("+str(self.resolution)+") - Edit"

    class Meta:
        verbose_name_plural ="BG Banner"

class NewsLetter(models.Model):
    site_info = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    resolution = models.CharField(max_length=50,default="760x800",editable=False,help_text="760x800, recomended resolution")
    image = models.ImageField(upload_to="site_config_img/images/",help_text="recomended resolution - 1920x900")

    def __str__(self):
        return "News Letter ("+str(self.resolution)+") - Edit"

    class Meta:
        verbose_name_plural ="News Letter"

class TitleOfFaq(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    discription = HTMLField()
    def __str__(self):
        return str((self.site))+" : FAQ Discription"

    class Meta:
        verbose_name_plural ="FAQ Title"

class Faq(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    question = models.CharField(max_length=150,help_text="Write Question")
    answer = HTMLField(help_text="Please write suitable answer..")
    def __str__(self):
        return str(self.site)+" : "+self.question[:10]+"..... ?"

    class Meta:
        verbose_name_plural ="FAQ"

class AboutSite(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    discription = HTMLField()
    def __str__(self):
        return str(self.site)+" : "+self.title

    class Meta:
        verbose_name_plural ="About Site"

class Subscriber(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    CHOICE = (('','Select Gender'),('M','Male'),('F','Female'),('O','Other'))
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50,choices=CHOICE,default="Select Gender")
    def __str__(self):
        return str(self.site)+" : "+self.email

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.email
    class Meta:
        # app_label="Contact Us"
        # verbose_name="Contact Us"
        verbose_name_plural ="Contact Us"

class ContactUsInfo(models.Model):
    contact_us = models.ForeignKey(ContactUs,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = HTMLField()
    at_date_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.subject

    class Meta:
        # app_label="Contact Us"
        # verbose_name="Contact Us"
        verbose_name_plural ="ContactUs Info"

class SiteOffer(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=models.CASCADE)
    offer_title = models.CharField(max_length=100,help_text="Ex - Globle Offer")
    offer_name = models.CharField(max_length=100,help_text="Ex- Official Launch Don't miss")
    offer_end = models.CharField(max_length=100,verbose_name="Offer End YYYY/MM/DD")
    def __str__(self):
        return str(self.site)+" : "+self.offer_title+" Offer"
    class Meta:
        # app_label="Contact Us"
        # verbose_name="Contact Us"
        verbose_name_plural ="Site Offer"



