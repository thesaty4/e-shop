import datetime
from time import time
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from accounts.models import BillingInfo
try: from accounts.models import User
except: i=0
# Create your models here.

#######################################These are Dynamic#######################################
class Category(models.Model):
    icon = models.CharField(max_length=50,help_text="icon text - fas fa-tv")
    category = models.CharField(max_length=100,help_text="Ex - ELECTRONICS, SPORTS, MEDICINE more")
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.category

class Subcategory(models.Model):
    product_categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=100)
    def __str__(self):
        return (self.subcategory)
        # return str(self.product_categories)+" : "+(self.subcategory)+" - EDIT"

class ProductBrand(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    def __str__(self):
        return self.brand
        # return str(self.category)+" : "+self.brand

class CategoryImage(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="category_image/")

    def __str__(self):
        return "IMAGE OF "+str(self.category)+" CATEGORY"
########################################These are Dynamic#######################################

from django.contrib import admin
from django.utils.html import format_html
#######################################PRODUCT MANAGEMENT TABLE#######################################
class Product(models.Model):
    CHOICE = (('','SELECT OFFER'),('YES','YES'),('NO','NO'))
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    # model = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    m_r_p = models.FloatField()
    discount_percentage = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    available_product = models.IntegerField()
    selled_product = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    is_offer = models.CharField(max_length=10,choices=CHOICE,default="SELECT OFFER")
    offer_end = models.CharField(max_length=100,null=True,blank=True,verbose_name="Offer End YYYY/MM/DD")
    color_code = models.CharField(max_length=100)
    shipping_charge = models.FloatField()
    tags = models.TextField(max_length=500)
    product_policy = models.TextField(max_length=200)
    image = models.ImageField(upload_to="product_manage_img/product_image/")
    video_url = models.URLField(null=True,blank=True)
    discription = models.TextField(max_length=1000)
    extra_info = models.TextField(max_length=1000,help_text="Enter value key1:'val1 val2', key2:'val1 val2'")
    # size = models.CharField(max_length=50,default='Not Available')
    # weight = models.CharField(max_length=50,default='Not Available')
    add_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.brand)

    @admin.display
    def item(self):
        return format_html("<img src='/media/%s' width='30' height='30' >"%(self.image))

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    img_path = models.ImageField(upload_to="product_manage_img/product_images/")
    def __str__(self):
        return "Image for "+str(self.product)

from tinymce.models import HTMLField
import uuid
######################START: CHECKOUT PROCESS###########################

class Checkout(models.Model):
    CHOICE = (('processing','Processing'),('shipped','Shipped'),('delivered','Delivered'),('cancel','Cancelled'),('return','Return'))

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingInfo,on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid1,unique=True,editable=False)
    transaction_id = models.UUIDField(default=uuid.uuid1,unique=True)
    quantity = models.BigIntegerField()
    tax = models.FloatField()
    color = models.CharField(max_length=255)
    total_amount = models.BigIntegerField()
    delevery_charge = models.BigIntegerField()
    delevery_mode = models.CharField(max_length=100)
    order_status = models.CharField(max_length=50,choices=CHOICE,default="processing")
    # disc = HTMLField()
    @admin.display
    def item(self):
        return format_html("<img src='/media/%s' width='30' height='30' >"%(self.product.image))
    def p(self):
        return format_html("<img src='/media/%s' width='30' height='30' >"%(self.customer_user.profile_pic))

    checkout_date_time = models.DateTimeField(default=datetime.datetime.now(),editable=False)
    def __str__(self):
        return str(self.order_id)

class CheckoutItemOwner(models.Model):
    checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    item_owner = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.checkout)

    class Meta:
        verbose_name_plural="item Owner"


class Office(models.Model):
    manager = models.ForeignKey(User,on_delete=models.CASCADE)
    office_code = models.IntegerField()
    pin_code = models.BigIntegerField()
    helpline_number = models.BigIntegerField()
    helpline_email = models.EmailField()
    full_address = HTMLField()
    def __str__(self):
        return str(self.office_code) 

class OrderTracking(models.Model):
    choice=(("arrived","Arrived"),('shipped','Shipped'),('nearest hub','Reach Nearest Hub'),("delivered","Finally Deliverd"),("cancel","Cancelled"))
    tracking_id = models.ForeignKey(Checkout,on_delete=models.CASCADE)
    office_code = models.ForeignKey(Office,on_delete=models.CASCADE)
    # latitude = models.CharField(max_length=100)
    # langitude = models.CharField(max_length=100)
    status = models.CharField(max_length=50,choices=choice,default="arrived")
    arrival_time = models.TimeField()
    arrival_date = models.DateField(default=datetime.date.today)
    leaved_time = models.TimeField()
    leaved_date = models.DateField()
    def __str__(self):
        return str(self.tracking_id)
    @admin.display
    def item(self):
        return format_html("<img src='/media/%s' width='30' height='30' >"%(self.tracking_id.product.image))

    class Meta:
        verbose_name_plural="Order Tracking"
#######################END: CHECKOUT PROCESS###############################

#######################START: PRODUCT REVIEW###############################
class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    review_rating = models.IntegerField()
    review_comment = models.TextField(max_length=500)
    review_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.product)+" review by "+str(self.customer_user)


class ReviewVote(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.ForeignKey(ProductReview,on_delete=models.CASCADE)
    is_up_vote = models.BooleanField()
    def __str__(self):
        return str(self.product)+"'s vote"
#######################END: PRODUCT REVIEW###############################

class Wishlist(models.Model):
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    is_wish = models.BooleanField(default=True)
    date_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.customer_user)+"'s wishlist"

class ProductSubscriber(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.user)+" has been subscribed "+str(self.product)

class ProductTags(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)+"'s Tag for "+str(self.product)

# THIS IS FOR LOGGIN USER
class ProductUserViews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    host_name=models.CharField(max_length=100)
    host_ip = models.GenericIPAddressField()
    def __str__(self):
        return "Product "+str(self.product)+", Viewer "+str(self.user)

# THIS IS FOR ANONYMOUS USER
class ProductViews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    host_name=models.CharField(max_length=100)
    host_ip = models.GenericIPAddressField()
    def __str__(self):
        return "Product "+str(self.product)+", Viewer "+str(self.host_name)

class TotalViews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    views = models.BigIntegerField()
    def __str__(self):
        return "Product "+str(self.product)+", Total Views = "+str(self.views)




