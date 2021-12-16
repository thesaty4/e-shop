from selling_product.models import OrderTracking
from selling_product.models import Checkout
from accounts.models import BillingInfo
from blogs.models import CommentVote
from blogs.models import CommentReply
import random
from selling_product.models import Subcategory,Category
from django.template import Library
from selling_product.models import ReviewVote, Product,ProductReview,ProductImage,Wishlist, ProductSubscriber, ProductReview
register = Library()
import requests
import urllib.parse
import datetime
from extraPackage.productAlgo import ArrivalProduct
# importing socket module
import socket
from django.template.loader import get_template
# def title(data):
#     return lower()
# register.filter(title)

def discount_calculate(val,discount):
    per = discount/100
    disc = per*val
    return round((val-disc),2)
register.filter(discount_calculate)

def percentage_calculate(amount,tax):
    per = tax/100
    t_tax = per*amount
    return round(t_tax,2)
register.filter(percentage_calculate)

def new_arrival_product_logged(uid,order_by):
    # ALL OF THESE DATA CAME FROM OUR ALGORITHEM
    if uid!='':
        products = ArrivalProduct(order_by).loggedUser(uid)
    else:
        products=[]
    return products
register.filter(new_arrival_product_logged)

import math
def discount(pid):
    p=Product.objects.get(id=pid)
    return math.floor(((p.m_r_p-p.price)/p.m_r_p)*100)
register.filter(discount)

def new_arrival_product_anonymous(hostname_ip,order_by):
    # ALL OF THESE DATA CAME FROM OUR ALGORITHEM
    if str(hostname_ip) != ',':
        host=str(hostname_ip).split(",")
        products = ArrivalProduct(order_by).anonymousUser(host[0],host[1])
    else:
        products = []
    return products
register.filter(new_arrival_product_anonymous)


def subcategory(categoryId):
    return Subcategory.objects.filter(product_categories=categoryId)
register.filter(subcategory)

def get_product_by_subcategory(scid):
    return Product.objects.filter(subcategory=scid).order_by('-id')[:5]
register.filter(get_product_by_subcategory)

def get_item_by_subcategory(scid):
    return Product.objects.filter(subcategory=scid).order_by('-id')[:5]
register.filter(get_item_by_subcategory)

def get_item_by_category(cid):
    return Product.objects.filter(category=cid).order_by('-id')[:5]
register.filter(get_item_by_category)

def get_all_item_by_category(cid):
    return Product.objects.filter(category=cid).order_by('-average_rating')
register.filter(get_all_item_by_category)

def all_product(total):
    arrival_products=Product.objects.all()
    return arrival_products
register.filter(all_product)

def product_rating(id):
    rating = ProductReview.objects.filter(product=id)
    return rating.count()
register.filter(product_rating)

def rating(id):
    PR = ProductReview.objects.filter(product=id).count()
    if PR == 0:
        return 0
    else:
        star1 = ProductReview.objects.filter(product=id,review_rating=1).count()
        star2 = ProductReview.objects.filter(product=id,review_rating=2).count()
        star3 = ProductReview.objects.filter(product=id,review_rating=3).count()
        star4 = ProductReview.objects.filter(product=id,review_rating=4).count()
        star5 = ProductReview.objects.filter(product=id,review_rating=5).count()
        # Avarage rating formula ar=1*star1+2*star2+3*star3+4*star4+5*star5/5
        AR=(1*star1+2*star2+3*star3+4*star4+5*star5)/(star1+star2+star3+star4+star5)
        return round(AR,1)
register.filter(rating)

def split_data(data,location):
    dataset = data.split(location)
    return dataset
register.filter(split_data)

def get_data_from_split(data,location):
    return data[location]
register.filter(get_data_from_split)

def get_product(id):
    product=Product.objects.filter(id=id)
    return product
register.filter(get_product)

def get_product_images(id):
    images=ProductImage.objects.filter(product=id)
    return images
register.filter(get_product_images)

def price_calculate(price,quantity):
    return float(price)*int(quantity)
register.filter(price_calculate)

def filter_wishlist(user_id,product_id):
    val = Wishlist.objects.filter(customer_user=user_id,product=product_id,is_wish=True)
    if val.count():
        return False
    else:
        return True 
register.filter(filter_wishlist)

def wishlist_data(user_id):
    data=Wishlist.objects.filter(customer_user=user_id).order_by("-id")
    return data
register.filter(wishlist_data)

def total_wishlist(user_id):
    data=Wishlist.objects.filter(customer_user=user_id)
    return data.count()
register.filter(total_wishlist)

def total_product_wishlist(product_id):
    data=Wishlist.objects.filter(product=product_id)
    return data.count()
register.filter(total_product_wishlist)

def filter_subscriber(uid,pid):
    data = ProductSubscriber.objects.filter(user=uid,product=pid)
    if data.count():
        return False
    else:
        return True 
register.filter(filter_subscriber)

def total_product_subscriber(pid):
    data = ProductSubscriber.objects.filter(product=pid)
    return data.count() 
register.filter(total_product_subscriber)

# PRICE SEPRATOR 100000 => 1,00,000 CONVERTER and 95000 = 9,5,000 
# THIS FUNCTION CONVERT VALUE AFTER THOUSEND
def to_comma_for_extra_comman(val):
    data = str(val).split(".")
    lsv = data[0]
    rsv = data[1]
    def rev(arg):                      # REVERSING NORMAL STRING
        c=0
        d=""
        for i in arg:
            c+=1
            d+=arg[-c]
        return d

    def rev_comma_value(arg):
        counter=0
        data=''
        for d in arg:
            if arg[len(arg)-1]==',' :
                arg=arg[0:len(arg)-1]
            else:
                if len(arg) > 3:
                    if counter == len(arg)-1:
                        if arg[counter] != ',' or arg[counter-1] !=',':
                            if arg[counter-1] != ',':
                                data+=","
                    data+=arg[counter]
                    counter+=1
                else:
                    data+=arg[counter]
                    counter+=1
        counter=1
        rev_data=''
        for rv in data:
            rev_data+=data[-counter]
            counter+=1
        return rev_data
        
    rev_data = rev(lsv)
    comma_data=''
    counter=1
    begining=0
    end=0
    position=0
    for i in rev_data:                           # MAKING SEPRATED STRING WITH COMMAN (,)
        if counter%3 == 0:                       # 2,333,334,444.0 IF STRING POSTION IN 3 DIGITS
            comma_data+=rev_data[begining:end+1] # SLICING DATA FROM REVERSE DATA
            comma_data+=","                      # APPENDING COMMAN (,)
            position+=3                          # INCREASING POSITION
        counter+=1
        begining=position                        
        end+=1
    else:
        comma_data+=rev_data[position:counter]      # APPENDING LAST VALUE OF STRING

    return rev_comma_value(comma_data)+"."+rsv # MAKING FINAL DATA
register.filter(to_comma_for_extra_comman)

# PRICE SEPRATOR 100000 => 1,00,000 CONVERTER and 95000 = 95,000
# THIS FUNCTION CONVERT VALUE AFTER THREE DIGITS
def to_comma(val):
    data = str(float(val)).split(".")
    lsv = data[0]
    rsv = data[1]
    def rev(arg):                      # REVERSING NORMAL STRING
        c=0
        d=""
        for i in arg:
            c+=1
            d+=arg[-c]
        return d

    def rev_comma_data(arg):             # METHOD FOR REVERSING COMMAN STRING
        counter=0
        data=""
        for d in arg:
            if arg[len(arg)-1]==',' :    # IF LAST VALUE IS COMMAN THEN REMOVE IT
                arg=arg[0:len(arg)-1]    # AND CREATING NEW STRING
            else:                        # IF LAST VALUE ISN'T COMMAN THEN DON'T REMOVE KEEP REVERSING
                counter+=1
                data+=arg[-counter]
        return data

    rev_data = rev(lsv)
    comma_data=''
    counter=1
    begining=0
    end=0
    position=0
    for i in rev_data:                           # MAKING SEPRATED STRING WITH COMMAN (,)
        if counter%3 == 0:                       # 2,333,334,444.0 IF STRING POSTION IN 3 DIGITS
            comma_data+=rev_data[begining:end+1] # SLICING DATA FROM REVERSE DATA
            comma_data+=","                      # APPENDING COMMAN (,)
            position+=3                          # INCREASING POSITION
        counter+=1
        begining=position                        
        end+=1
    else:
        comma_data+=rev_data[position:counter]      # APPENDING LAST VALUE OF STRING

    return rev_comma_data(comma_data)+"."+rsv # MAKING FINAL DATA
register.filter(to_comma)

def cvt_comma(val):

    lsv = str(val)
    def rev(arg):                      # REVERSING NORMAL STRING
        c=0
        d=""
        for i in arg:
            c+=1
            d+=arg[-c]
        return d

    def rev_comma_data(arg):             # METHOD FOR REVERSING COMMAN STRING
        counter=0
        data=""
        for d in arg:
            if arg[len(arg)-1]==',' :    # IF LAST VALUE IS COMMAN THEN REMOVE IT
                arg=arg[0:len(arg)-1]    # AND CREATING NEW STRING
            else:                        # IF LAST VALUE ISN'T COMMAN THEN DON'T REMOVE KEEP REVERSING
                counter+=1
                data+=arg[-counter]
        return data

    rev_data = rev(lsv)
    comma_data=''
    counter=1
    begining=0
    end=0
    position=0
    for i in rev_data:                           # MAKING SEPRATED STRING WITH COMMAN (,)
        if counter%3 == 0:                       # 2,333,334,444.0 IF STRING POSTION IN 3 DIGITS
            comma_data+=rev_data[begining:end+1] # SLICING DATA FROM REVERSE DATA
            comma_data+=","                      # APPENDING COMMAN (,)
            position+=3                          # INCREASING POSITION
        counter+=1
        begining=position                        
        end+=1
    else:
        comma_data+=rev_data[position:counter]      # APPENDING LAST VALUE OF STRING

    return rev_comma_data(comma_data)# MAKING FINAL DATA
register.filter(cvt_comma)

def add(val1,val2):
    return int(val1)+int(val2)
register.filter(add)

def addFlt(v1,v2):
    return float(v1)+float(v2)
register.filter(addFlt)

def concat_limit(val1,val2):
    return str(val1)+":"+str(val2)
register.filter(concat_limit)



def sub(val1,val2):
    return int(val1)-int(val2)
register.filter(sub)

def div(val1,val2):
    return round(int(val1)/int(val2))
register.filter(div)

def rnd(data):
    return round(data)
register.filter(rnd)

def mul(val1,val2):
    return float(val1)*int(val2)
register.filter(mul)

def get_review_by_user(pid,uid):
    obj = ProductReview.objects.filter(product=pid,customer_user=uid)
    return obj
register.filter(get_review_by_user)

def filter_review(pid):
    obj = ProductReview.objects.filter(product=pid).order_by("-review_rating")
    return obj
register.filter(filter_review)

def object_count(data):
    return data.count()
register.filter(object_count)

def rating_avg(pid):
    PR = ProductReview.objects.filter(product=pid).count()
    if PR == 0:
        return 0
    else:
        star1 = ProductReview.objects.filter(product=pid,review_rating=1).count()
        star2 = ProductReview.objects.filter(product=pid,review_rating=2).count()
        star3 = ProductReview.objects.filter(product=pid,review_rating=3).count()
        star4 = ProductReview.objects.filter(product=pid,review_rating=4).count()
        star5 = ProductReview.objects.filter(product=pid,review_rating=5).count()
        # Avarage rating formula ar=1*star1+2*star2+3*star3+4*star4+5*star5/5
        AR=(1*star1+2*star2+3*star3+4*star4+5*star5)/(star1+star2+star3+star4+star5)
        return round(AR,1)
register.filter(rating_avg)

def price_round(price,round_value):
    return round(price,round_value)
register.filter(price_round)

def check_review(pid,uid):
    obj = ProductReview.objects.filter(customer_user=uid,product=pid)
    return obj.count()
register.filter(check_review)

def get_vote_by_review(rid):
    obj = ReviewVote.objects.filter(review=rid)
    return obj
register.filter(get_vote_by_review)

def get_upvote_by_review(rid):
    obj = ReviewVote.objects.filter(review=rid,is_up_vote=True)
    return obj
register.filter(get_upvote_by_review)

def get_downvote_by_review(rid):
    obj = ReviewVote.objects.filter(review=rid,is_up_vote=False)
    return obj
register.filter(get_downvote_by_review)

def check_upvote_by_user(uid,rid):
    obj = ReviewVote.objects.filter(customer_user=uid,review=rid,is_up_vote=True)
    return obj.count()
register.filter(check_upvote_by_user)
    
def check_downvote_by_user(uid,rid):
    obj = ReviewVote.objects.filter(customer_user=uid,review=rid,is_up_vote=False)
    return obj.count()
register.filter(check_downvote_by_user)
    


# REGISTERING SIMPLE TAG
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

from django.contrib.auth import get_user_model
# from django import template
# register = template.Library()
def show_users_table():
    User = get_user_model()
    users = User.objects.all()
    return {'users': users}
users_template = get_template('inclusion_tags/user.html')
register.inclusion_tag(users_template)(show_users_table)

def host_details(temp):
    return str(socket.gethostname()+","+socket.gethostbyname(socket.gethostname()))
register.filter(host_details)

@register.simple_tag
def get_host_ip():
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    # print(f"Hostname: {hostname}")
    # print(f"IP Address: {ip_address}")
    return str(hostname)+","+str(ip_address)

def get_lat_long(address,url):
    address = 'Shivaji Nagar, Bangalore, KA 560001'
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    print(response[0]["lat"])
    print(response[0]["lon"])
    return str(response[0]['lat'])+","+str(response[0]['lon'])
register.filter(get_lat_long)

def get_review(pid):
    return ProductReview.objects.filter(product=pid)
register.filter(get_review)

def make_list(data):
    lst=[]
    for i in range(1,data+1,1):
        lst.append(i)
    return lst
register.filter(make_list)

def length(data):
    return len(data)
register.filter(length)

# from selling_product.models import ProductUserViews,ProductViews
# from selling_product.views import meta_data
# from accounts.views import User
# def customer_also_viewed(uid,shopname):
#     # products = ProductViews.objects.all().select_related("product").order_by("-id")[0:10]
#     # THIS PRODUCT GOES FOR USER ALSO VIEWD
#     products = Product.objects.all().order_by("-id")[0:10]
#     if products.count() == 0:
#         products = Product.objects.all().order_by("-id")[0:10]
#     # print("user => "+str(user)+", shop=>"+str(shopname))
#     user = User.objects.get(id=uid)
#     return {'user':user,'products':products,'site_info_data':shopname}
# template = get_template("inclusion_tags/customer-also-views.html")
# register.inclusion_tag(template)(customer_also_viewed)
from django.db.models import Q
@register.simple_tag
def fetch_item_rating(rate,query):
    if query=='' or query==None:
        return Product.objects.filter(Q(average_rating__gte=rate) or Q(average_rating__lt=int(rate)+1)).count()
    else:
        # SUSPICIOUS -------------->>>>>>>>>>>>>
        # return Product.objects.filter(Q(average_rating__gte=rate) or Q(average_rating__lt=int(rate)+1)).count()
        return Product.objects.filter(Q(average_rating__gte=rate) or Q(average_rating__lt=int(rate)+1) and Q(tags__contains=query) or Q(discription__contains=query) or Q(price__contains=query or Q(m_r_p__contains=query) or Q(discount_percentage__contains=query) or Q(extra_info__contains=query) or Q(title__contains=query))).count()
# register.filter(fetch_item_rating)

from EshopApp.models import ShopByDealsImage
# @register.simple_tag
def get_image_of__shop_by_deal(site,lable):
    return ShopByDealsImage.objects.get(site=site,lable=lable)
register.filter(get_image_of__shop_by_deal)

def get_product_for_deal_of_day(slc):
    return Product.objects.filter(is_offer='YES').order_by('-offer_end')[:slc]
register.filter(get_product_for_deal_of_day)

def rev_date(data):
    d=data.split("/")
    return d[0]+"/"+d[1]+'/'+d[2]
register.filter(rev_date)

def featured_products(slc):
    categories = Category.objects.all()
    products=[]
    product_ids=[]
    for category in categories:
        p=Product.objects.filter(category=category.id).order_by('-average_rating','-add_date_time')[:1]
        products.extend(list(p))
        for pid in p:
            product_ids.append(pid.id)

    prdct=Product.objects.all().order_by('-average_rating','-add_date_time')
    if len(products) != 4:
        for product in prdct:
            if len(products) == 4:
                break
            else:
                # BEFORE APPENDING NEW PRODUCT, WE CHECK DOUBLYCACY AND FILTER THEM
                if product.id not in product_ids:
                    products.extend(list(Product.objects.filter(id=product.id)))

    return products[:slc]
register.filter(featured_products)
    
@register.simple_tag
def get_highest_discount():
    product=Product.objects.all().order_by("-discount_percentage")[1]
    return product.discount_percentage

@register.simple_tag
def get_highest_discount_category():
    product=Product.objects.all().order_by("-discount_percentage")[1]
    return product.category

from random import randint
def get_weekly_products(slc):
    products=Product.objects.all().order_by("-add_date_time","-id")[:7]
    newProduct=[]
    num=[]
    for i in range(0,slc):
        randnum=randint(0,6)
        num.append(randnum)
        if randnum not in num:
            newProduct.append(products[randnum])
        else:
            randnum=randint(0,6)
            if randnum not in num:
                newProduct.append(products[randnum])
            else:
                randnum=randint(0,6)
                if randnum not in num:
                    newProduct.append(products[randnum])
                else:
                    randnum=randint(0,6)
                    if randnum not in num:
                        newProduct.append(products[randnum])
    return newProduct
register.filter(get_weekly_products)

def get_flash_products(slc):
    products=Product.objects.all().order_by("-id")
    newProduct=[]
    num=[]
    for i in range(0,slc):
        randnum=randint(0,int(products.count())-1)
        num.append(randnum)
        if randnum not in num:
            newProduct.append(products[randnum])
        else:
            randnum=randint(0,int(products.count())-1)
            if randnum not in num:
                newProduct.append(products[randnum])
            else:
                randnum=randint(0,int(products.count())-1)
                if randnum not in num:
                    newProduct.append(products[randnum])
                else:
                    randnum=randint(0,int(products.count())-1)
                    if randnum not in num:
                        newProduct.append(products[randnum])
    return newProduct
register.filter(get_flash_products)

def get_special_products(slc):
    products=Product.objects.all().order_by("-id","-average_rating")
    newProduct=[]
    num=[]
    for i in range(0,slc):
        randnum=randint(0,int(products.count())-1)
        num.append(randnum)
        if randnum not in num:
            newProduct.append(products[randnum])
        else:
            randnum=randint(0,int(products.count())-1)
            if randnum not in num:
                newProduct.append(products[randnum])
            else:
                randnum=randint(0,int(products.count())-1)
                if randnum not in num:
                    newProduct.append(products[randnum])
                else:
                    randnum=randint(0,int(products.count())-1)
                    if randnum not in num:
                        newProduct.append(products[randnum])
    return newProduct
register.filter(get_special_products)

from blogs.models import Blog,Comment
def get_blogs(slice):
    return Blog.objects.all().order_by("-id")[:slice]
register.filter(get_blogs)

def get_user_blogs(uid):
    return Blog.objects.filter(customer_user=uid).order_by("-id")
register.filter(get_user_blogs)

def get_all_blogs(val):
    return Blog.objects.all().order_by("-id")
register.filter(get_all_blogs)

def get_all_blogs_count(val):
    return Blog.objects.all().count()
register.filter(get_all_blogs_count)

def get_blog_comments(id):
    return Comment.objects.filter(blogs=id)
register.filter(get_blog_comments)

def get_blog_comment_by_user(uid,bid):
    return Comment.objects.filter(customer_user=uid,blogs=bid)
register.filter(get_blog_comment_by_user)

def get_blog_comment(id,bid):
    return Comment.objects.filter(customer_user=id,blogs=bid).order_by("-id")
register.filter(get_blog_comment)

def get_blog_comment_reply(id):
    return CommentReply.objects.filter(blogs_comment=id).order_by("-id")
register.filter(get_blog_comment_reply)


def gt(val1,val2):
    if val1 > val2:
        return True
    else:
        return False
register.filter(gt)


def get_comment_upvote_by_user(bid,uid,cid):
    return CommentVote.objects.filter(blogs=bid,comment=cid,customer_user=uid,is_up_vote=True)

def get_comment_downvote_by_user(bid,uid,cid):
    return CommentVote.objects.filter(blogs=bid,comment=cid,customer_user=uid,is_up_vote=False)

def get_comment_total_upvote(bid,cid):
    return CommentVote.objects.filter(blogs=bid,comment=cid,is_up_vote=True)
register.filter(get_comment_total_upvote)

def get_comment_total_downvote(bid,cid):
    return CommentVote.objects.filter(blogs=bid,comment=cid,is_up_vote=False)
register.filter(get_comment_total_downvote)


def get_comment_upvote(info,uid):
    data = info.split(":")
    return get_comment_upvote_by_user(data[0],uid,data[1])
register.filter(get_comment_upvote)

def get_comment_downvote(info,uid):
    data = info.split(":")
    return get_comment_downvote_by_user(data[0],uid,data[1])
register.filter(get_comment_downvote)

from blogs.models import Vote
def get_blog_vote(data,tag):
    sdata = data.split(":")
    bid=sdata[0]
    uid=sdata[1]
    if tag == 'upvote':
        return Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=True)
    elif tag == 'downvote':
        return Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=False)
register.filter(get_blog_vote)

def get_blog_total_vote(bid,tag):
    if tag == 'upvote':
        return Vote.objects.filter(blogs=bid,is_up_vote=True)
    elif tag == 'downvote':
        return Vote.objects.filter(blogs=bid,is_up_vote=False)
register.filter(get_blog_total_vote)

def who_mentioned_me(user):
    user='@'+user
    CommentReply.objects.filter(comment_reply__contains=user)
register.filter(who_mentioned_me)

def who_commented_at_myblog(uid):
    blogs=Blog.objects.filter(customer_user=uid).order_by("-id")
    blog_ids=[]
    for blog in blogs:
        blog_ids.append(blog.id)

    blogComments=[]
    for bid in blog_ids:
        blogComments.extend(list(Comment.objects.filter(blogs=bid)))
    return blogComments
register.filter(who_commented_at_myblog)

def get_recent_blog(uid):
    return Blog.objects.filter(customer_user=uid).order_by("-id")
register.filter(get_recent_blog)


def get_total_product(uid):
    return Product.objects.filter(customer_user=uid).count()
register.filter(get_total_product)

def get_filter_total_product(uid):
    return Product.objects.filter(customer_user=uid,available_product__gt=0).count()
register.filter(get_filter_total_product)

def shipping_info(uid):
    return BillingInfo.objects.filter(user=uid,is_shipping_details=True)
register.filter(shipping_info)

def billing_info(uid):
    return BillingInfo.objects.filter(user=uid,is_billing_details=True)
register.filter(billing_info)

from django.template.defaultfilters import capfirst, stringfilter
import re
@register.filter(name='nbsp2space', is_safe=True)
@stringfilter
def nbsp2space(value):
    return re.sub('&nbsp;', ' ', value, flags=re.IGNORECASE)


import numpy as np 
import matplotlib.pyplot as plt
import base64
from io import BytesIO
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, formate="png")
    buffer.seek(0)
    image_png=buffer.getvalue()
    # print(image_png)
    graph = base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    # print(graph)
    buffer.close()
    return graph

from selling_product.models import Product
def bar_chart(val):
    subjects = ("python","c++","java","perl")
    y_pos = np.array(len(subjects))
    performance = [10,8,6,4]
    products=[]
    date = []
    all_product = Product.objects.all()
    for product in all_product:
        p_date=product.add_date_time.date()
        date.append(p_date)
        products.append(Product.objects.filter(add_date_time__contains=p_date).count())

    x=products
    y=date
    plt.grid(color="y",linestyle="--",linewidth=2,axis="y",alpha=1)
    plt.plot(y,x)
    # # plt.xtricks(y_pos,subjects)
    # plt.ylabel["usage"]
    # plt.title("Programming Languge")
    # print("bar chart is here...")

    # plt.switch_backend("AGG")
    # plt.figure(figsize=(10,4))
    # plt.plot(subjects,performance)
    return get_graph()
    # plt.show()
register.filter(bar_chart)

def minus(val1,val2):
    return val1-val2
register.filter(minus)

class CTR:
    variable = []
    def __init__(self,value):
        super.variable.append(value)

def counter(num):
    obj = CTR(num)

def get_my_order(uid):
    return Checkout.objects.filter(customer_user=uid).order_by("-id")
register.filter(get_my_order)

def track_order(id):
    return OrderTracking.objects.filter(tracking_id=id).order_by("arrival_date")
register.filter(track_order)
    
def counter(data):
    return data.count()
register.filter(counter)
from django.db.models import Q
def cancelled_checkout(uid):
    return Checkout.objects.filter(customer_user=uid,order_status='cancel')
register.filter(cancelled_checkout)

def returning_checkout(uid):
    return Checkout.objects.filter(customer_user=uid,order_status='return')
register.filter(returning_checkout)

from selling_product.models import CheckoutItemOwner
def numberOfCheckout(pid,uid):
    return CheckoutItemOwner.objects.filter(product=pid,item_owner=uid).count()
register.filter(numberOfCheckout)

# this filter give all checkout of my selled product
def get_our_items_checkout(uid):
    cio= CheckoutItemOwner.objects.filter(item_owner=uid)
    products=[]
    for data in cio:
        products.extend(list(Checkout.objects.filter(order_id=data.checkout.order_id,order_status='return')))
    return len(products)
register.filter(get_our_items_checkout)

def get_product_owner(order_id):
    cio = CheckoutItemOwner.objects.filter(checkout=order_id)
    owner=''
    for data in cio:
        owner+=str(capfirst(data.product.customer_user.first_name))+" "+str(capfirst(data.product.customer_user.last_name))
        break
    return owner
register.filter(get_product_owner)

def get_product_owner_mail(order_id):
    cio = CheckoutItemOwner.objects.filter(checkout=order_id)
    owner=''
    for data in cio:
        owner+=str(data.product.customer_user.email)
        break
    return owner
register.filter(get_product_owner_mail)

def get_product_owner_id(order_id):
    cio = CheckoutItemOwner.objects.filter(checkout=order_id)
    owner_id=''
    for data in cio:
        owner_id=data.product.customer_user.id
        break
    return owner_id
register.filter(get_product_owner_id)

def get_user_address(uid):
    add = BillingInfo.objects.filter(user=uid).order_by("-id")
    address=[]
    for a in add:
        address.append(a.full_address)
        break
    
    return address[0]

register.filter(get_user_address)

def get_hold_delivery(uid):
    processing=0
    owner_products = Product.objects.filter(customer_user=uid)
    for product in owner_products:
        cio=CheckoutItemOwner.objects.filter(item_owner=uid,product=product.id)
        for sells in cio:
            prc = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='processing').count()
            # ship = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='shipped').count()
            # deli = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='delivered').count()
            # canc = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='cancel').count()
            # ret = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='return').count()
            if(prc != 0):
                processing+=1
    return processing
register.filter(get_hold_delivery)

def get_my_items_checkout(uid):
    cio= CheckoutItemOwner.objects.filter(item_owner=uid)
    products=[]
    for data in cio:
        products.extend(list(Checkout.objects.filter(order_id=data.checkout.order_id,order_status='processing')))
    return reversed(products)
register.filter(get_my_items_checkout)

def returns_product(uid):
    owner_products = Product.objects.filter(customer_user=uid)
    checkouts = []
    for product in owner_products:
        checkout = Checkout.objects.filter(product=product.id,order_status='return')
        checkouts.extend(list(checkout))
    return reversed(checkouts)
register.filter(returns_product)

def total_returns(uid):
    owner_products = Product.objects.filter(customer_user=uid)
    checkouts = []
    for product in owner_products:
        checkout = Checkout.objects.filter(product=product.id,order_status='return')
        checkouts.extend(list(checkout))
    return len(checkouts)
register.filter(total_returns)

def get_total_purchease(uid,owner_id):
    checkouts = CheckoutItemOwner.objects.filter(item_owner=owner_id)
    total_checkout = 0
    for checkout in checkouts:
        order = Checkout.objects.filter(product=checkout.product,customer_user=uid).count()
        total_checkout+=order
    return total_checkout
register.filter(get_total_purchease)
    
def item_qty(item):
    checkouts =  Checkout.objects.filter(product=item)
    qty=0
    for checkout in checkouts:
        qty+=checkout.quantity
    return qty
register.filter(item_qty)