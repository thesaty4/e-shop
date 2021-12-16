from django import forms
from django.forms import ModelForm
from .models import Product,ProductImage
from PIL import Image
class ProductForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = Product
        fields = ('title','customer_user','color_code','category','subcategory','tax','brand','is_offer','available_product','price','shipping_charge','m_r_p','extra_info','image','x','y','width','height','video_url','product_policy','tags','discription','offer_end',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subcategory'].queryset = Subcategory.objects.none()
    #     self.fields['brand'].queryset = ProductBrand.objects.none()

    def save(self):
        photo = super(ProductForm,self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        img = Image.open(photo.image)
        cropped_image = img.crop((x,y,w+x,h+y))
        resized_image = cropped_image.resize((600,600),Image.ANTIALIAS)
        resized_image.save(photo.image.path)
        return photo

class ProductImageForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = ProductImage
        fields = ("product",'img_path','x','y','width','height',)

    def save(self):
        photo = super(ProductImageForm,self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        img = Image.open(photo.img_path)
        cropped_image = img.crop((x,y,w+x,h+y))
        resized_image = cropped_image.resize((1600,1600),Image.ANTIALIAS)
        resized_image.save(photo.img_path.path)
        return photo

# EDIT
class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title','customer_user','color_code','tax','category','subcategory','brand','is_offer','available_product','price','shipping_charge','m_r_p','extra_info','video_url','product_policy','tags','discription','offer_end',)

class ProductEditImageForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = Product
        fields = ('image','x','y','width','height',)

    def save(self):
        photo = super(ProductEditImageForm,self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        img = Image.open(photo.image)
        cropped_image = img.crop((x,y,w+x,h+y))
        resized_image = cropped_image.resize((600,600),Image.ANTIALIAS)
        resized_image.save(photo.image.path)
        return photo

