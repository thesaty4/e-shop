from django import forms
from django.db import models
from django.forms import ModelForm, fields
from PIL import Image
from .models import Blog
from tinymce.widgets import TinyMCE
  
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class BlogForm(ModelForm):
    discription = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    x=forms.FloatField(widget=forms.HiddenInput())
    y=forms.FloatField(widget=forms.HiddenInput())
    width=forms.FloatField(widget=forms.HiddenInput())
    height=forms.FloatField(widget=forms.HiddenInput())

    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    
    class Meta:
        model=Blog
        fields=('customer_user','title','tags','image','audio','video','discription',)
        # fields='__all__'

    def save(self):
        photo=super(BlogForm,self).save()
        x=self.cleaned_data.get('x')
        y=self.cleaned_data.get('y')
        w=self.cleaned_data.get('width')
        h=self.cleaned_data.get('height')
        img = Image.open(photo.image)
        cropped_image = img.crop((x,y,w+x,h+y))
        resized_image = cropped_image.resize((900,500),Image.ANTIALIAS)
        resized_image.save(photo.image.path)
        return photo

class BlogImageForm(ModelForm):
    x=forms.FloatField(widget=forms.HiddenInput())
    y=forms.FloatField(widget=forms.HiddenInput())
    width=forms.FloatField(widget=forms.HiddenInput())
    height=forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model=Blog
        fields=('customer_user','title','tags','image','discription',)

    def save(self):
        photo=super(BlogImageForm,self).save()
        x=self.cleaned_data.get('x')
        y=self.cleaned_data.get('y')
        w=self.cleaned_data.get('width')
        h=self.cleaned_data.get('height')
        img = Image.open(photo.image)
        cropped_image = img.crop((x,y,w+x,h+y))
        resized_image = cropped_image.resize((900,500),Image.ANTIALIAS)
        resized_image.save(photo.image.path)
        return photo

class BlogAudioForm(ModelForm):
    class Meta:
        model=Blog
        fields=('customer_user','title','tags','audio','discription',)

class BlogOnlyFrom(ModelForm):
    class Meta:
        model=Blog
        fields=('customer_user','title','tags','image','discription',)