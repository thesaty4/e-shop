from django import forms
from django.db import models
from django.forms import ModelForm
from .models import User
from PIL import Image
# for image cropper

class Customer_reg_form(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput(),}
        fields = ("username","first_name","last_name","email","gender","dob","country","password","profile_pic","x","y","width","height")

    def save(self):
        photo = super(Customer_reg_form, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = Image.open(photo.profile_pic)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)
        resized_image.save(photo.profile_pic.path)
        return photo
