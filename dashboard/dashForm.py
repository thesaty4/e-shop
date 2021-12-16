from django.contrib.auth import models
from django.db.models import fields
from django import forms
from django.forms import ModelForm
from django.forms.widgets import Widget
from accounts.models import User,BillingInfo
from PIL import Image

class UserInfo(ModelForm):
    class Meta:
        model=User
        fields = ('username','email','first_name','last_name','gender','dob','country')

class UpdateProfilePic(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = User
        fields = ("profile_pic","x","y","width","height")

    def save(self):
        photo = super(UpdateProfilePic, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = Image.open(photo.profile_pic)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        resized_image.save(photo.profile_pic.path)
        return photo

class BillingInfoFrom(ModelForm):
    class Meta:
        model = BillingInfo
        fields = ("id","first_name","last_name","mobile","country","state","pin_code","full_address",)
