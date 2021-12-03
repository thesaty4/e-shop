from django.db import models
from django.db.models.deletion import CASCADE
import datetime
from EshopApp.models import *
from django_countries.fields import CountryField
# Primary key
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html, html_safe
from django.contrib import admin
class User(AbstractUser):
    GENDER = (('','Select Gender'),('M','Male'),('F','Female'),('O','Other'))
    gender = models.CharField(max_length=50,choices=GENDER,default='Select Gender')
    dob = models.DateField(default=datetime.datetime.now(),null=True,blank=True)
    profile_pic = models.ImageField(upload_to="profile/")
    account_status = models.BooleanField(default=True)
    position = models.CharField(max_length=120,help_text="What is your corrent position(Ex. Software Eng.)?",null=True,blank=True)
    country = CountryField()
    twitter = models.CharField(max_length=100,default='#',help_text="https:/twitter.com/(USER_ID) - Put Only USER_ID")
    facebook = models.CharField(max_length=100,default='#',help_text="https:/facebook.com/(USER_ID) - Put Only USER_ID")
    instagram = models.CharField(max_length=100,default='#',help_text="https:/instagram.com/(USER_ID) - Put Only USER_ID")
    linkedin = models.CharField(max_length=100,default='#',help_text="https:/linkedin.com/(USER_ID) - Put Only USER_ID")
    password = models.CharField(max_length=300)
    reg_date_time = models.DateTimeField(default=datetime.datetime.now())
    # def __str__(self):
    #     return '<img src="/media/%s" width="50" height="50" />'%self.profile_pic
    
    @admin.display
    def profile(self):
        return format_html('<img src="/media/%s" width="30" height="30" />'%(self.profile_pic))
    #     if self.profile_pic:
    #     else:
    #         return mark_safe('<img src="" width="50" height="50" />'%(self.profile_pic))
    # pic.short_discription="Image"
        
        


# Foreign Table of users
class BillingInfo(models.Model):
    CHOICE = (('','SELECT STATE'),('AP',"ANDHRA PRADESH"),('UP','UTTAR PRADESH'),('MP','MADHYA PRADESh'))
    user = models.ForeignKey(User,on_delete=CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=20,help_text="Write your number in Internation Format (+)")
    country = CountryField()
    state = models.CharField(max_length=100,choices=CHOICE,default='SELECT STATE')
    pin_code = models.CharField(max_length=10)
    is_shipping_details = models.BooleanField(default=True)
    is_billing_details = models.BooleanField(default=True)
    full_address = models.TextField(max_length=500)

    def __str__(self):
        return str(self.user)+" - information"
    @admin.display
    def profile(self):
        return format_html('<img src="/media/%s" width="30" height="30" />'%(self.user.profile_pic))