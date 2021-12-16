from selling_product.models import OrderTracking
from selling_product.models import Checkout
from accounts.models import BillingInfo
from selling_product.models import ProductUserViews, ProductReview, TotalViews
from selling_product.models import Product,TotalViews,ProductViews
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import SiteInfo,Subscriber,SiteOffer,AboutSite,Faq,TitleOfFaq,ContactUsInfo,ContactUs,Slider,BackgroundBanner,NewsLetter
from selling_product.models import ReviewVote,ProductReview,ProductTags, Category,Subcategory,CategoryImage,ProductImage, Product
from Feedback.models import UserFeedback
from accounts.models import User
from extraPackage.auth import dataValidate
from extraPackage.productAlgo import Rating
from django.db.models import Q
site_info_data = SiteInfo.objects.last()
latestSite = SiteInfo.objects.last()                                 # Descending order data fatch
productsData=Product.objects.select_related("category","subcategory").order_by('-id')[:10]

# Create your views here.

def meta_data():
    try: category = Category.objects.all()
    except Category.DoesNotExist: category=False
    try: subcategory = Subcategory.objects.all()
    except Subcategory.DoesNotExist: subcategory=False

    try: category_image = CategoryImage.objects.all()
    except CategoryImage.DoesNotExist: category_image=False

    return {
        'category':category,
        'subcategory':subcategory,
        'category_image':category_image
}

def index(request):
    if request.method == "POST":
        ############# FOR SUBSCRIBING AJAX FORM REQUEST #################
        gender = request.POST['gender'].strip().upper()
        email = request.POST['email'].strip().lower()
        sub_obj = Subscriber.objects.filter(email=email)
        if sub_obj.count() > 0 :
            status_code = 400
            message = "email exists"
            explanation = "Given Email are already subscribed"
            return JsonResponse({'message':message,'explanation':explanation},status=status_code)
        else:
            sb = Subscriber(email=email,gender=gender)
            sb.save()
            return HttpResponse("")
    else:
        myoffer = SiteOffer.objects.filter(site=latestSite).last()
        slider = Slider.objects.filter(site_info=latestSite)
        if slider.count() == 0:
            slider = False

        try:background_banner = BackgroundBanner.objects.filter(site_info=latestSite).last()
        except BackgroundBanner.DoesNotExist:background_banner = False
        
        try:usr_feedback = UserFeedback.objects.all().select_related("user").order_by('id')[:5]
        except Exception: usr_feedback = UserFeedback.objects.all().select_related("user").order_by('id')
        
        try: newsletter=NewsLetter.objects.filter(site_info=latestSite).last()
        except NewsLetter.DoesNotExist:newsletter=False

        return render(request,"index.html",{
            'site_info_data':site_info_data,
            'slider':slider,
            'background_banner':background_banner,
            'myoffer':myoffer,
            'newsletter':newsletter,
            'usr_feedback':usr_feedback,
            'product_meta_data':meta_data(),
            'products_data':productsData
        })

def productDetails(request,product_id):
    product = Product.objects.get(id=product_id)
    images = ProductImage.objects.filter(product=product_id)
    shop = site_info_data.shop_name
    tags = ProductTags.objects.filter(product=product_id)
    start_limit = 0
    end_limit = 2

    # THIS QUERYSET GOES FOR USER ALSO VIEWD (PRODUCTS)
    puvList = []
    puvData = ProductUserViews.objects.all()
    for puv in puvData:
        if puv.product.id not in puvList:
            puvList.append(puv.product.id)

    item_also_viewed = []
    for productId in puvList:
        item_also_viewed.extend(list(Product.objects.filter(id=productId)))

    # IF NO ANY USER AVAILABLE IN WATCHLIST, THEN GET PRODUCT ID FROM ANONYMOUS USER VIEWD
    if len(item_also_viewed) < 10:
        pavData = ProductViews.objects.all()
        for pav in pavData:
            if pav.product.id not in puvList:
                puvList.append(pav.product.id)

        # RESET ITEM AND APPEND NEW DATA
        item_also_viewed=[]
        for productId in puvList:
            item_also_viewed.extend(list(Product.objects.filter(id=productId)))
    
    # # EITHER PRODUCT LESS THAN 10 PRODUCT, THEN APPEND MORE DATA IN THIS QUERYSET
    # if item_also_viewed.count < 10:
        
    return render(request,'product-detail.html',{
        'site_info_data':site_info_data,
        'product':product,
        'products':item_also_viewed,
        'product_images':images,
        'shop':shop,'product_meta_data':meta_data(),
        'tags':tags,'start_limit':start_limit,'end_limit':end_limit})

def shop(request):
    return render(request,'shop-list-left.html',{'site_info_data':site_info_data,
    'product_meta_data':meta_data()
    })

def wishlist(request):
    return render(request,"wishlist.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def checkout(request,pid):
    product = Product.objects.filter(id=pid)
    deadline = 0
    qty = 1
    for i in product:
        if qty> i.available_product:
            qty = i.available_product
        deadline = i.available_product
    return render(request,"checkout.html",{'site_info_data':site_info_data,'product_meta_data':meta_data(),'pid':pid,'quantity':qty,'deadline':deadline})

def checkoutQty(request,pid,qty):
    product = Product.objects.filter(id=pid)
    deadline = 0
    for i in product:
        if qty> i.available_product:
            qty = i.available_product
        deadline = i.available_product

    return render(request,"checkout.html",{'site_info_data':site_info_data,'product_meta_data':meta_data(),'pid':pid,'quantity':qty,'deadline':deadline})

def checkoutAll(request):
    return render(request,"checkout.html",{
        'site_info_data':site_info_data,
        'product_meta_data':meta_data(),
        'is_all_checkout':True      
        })
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
#     billing_address = models.ForeignKey(BillingInfo,on_delete=models.CASCADE)
#     order_id = models.UUIDField(default=uuid.uuid1,unique=True,editable=False)
#     transaction_id = models.UUIDField(default=uuid.uuid1,unique=True)
#     quantity = models.BigIntegerField()
#     tax = models.FloatField()
#     color = models.CharField(max_length=255)
#     total_amount = models.BigIntegerField()
#     delevery_charge = models.BigIntegerField()
#     delevery_mode = models.CharField(max_length=100)
#     order_status = models.CharField(max_length=50,choices=CHOICE,default="Pending")

from reportlab.pdfgen import canvas
def invoice():
    # Importing Required Module
    # Creating Canvas
    c = canvas.Canvas("invoice.pdf",pagesize=(200,250),bottomup=0)

    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10,40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("media/"+str(latestSite.logo),0,0,width=50,height=30)
    # c.drawImage("/",0,0,width=50,height=30)

    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10,-40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",10)
    # Inserting the name of the company
    c.drawCentredString(125,20,"XYZ PRIVATE LIMITED")
    # For under lining the title
    c.line(70,22,180,22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold",5)
    c.drawCentredString(125,30,"Block No. 101, Triveni Apartments, Pitam Pura,")
    c.drawCentredString(125,35,"New Delhi - 110034, India")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold",6)
    c.drawCentredString(125,42,"GSTIN : 07AABCS1429B1Z")

    # Line Seprating the page header from the body
    c.line(5,45,195,45)

    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold",8)
    c.drawCentredString(100,55,"TAX-INVOICE")

    # This Block Consist of Costumer Details
    c.roundRect(15,63,170,40,10,stroke=1,fill=0)
    c.setFont("Times-Bold",5)
    c.drawRightString(70,70,"INVOICE No. :")
    c.drawRightString(70,80,"DATE :")
    c.drawRightString(70,90,"CUSTOMER NAME :")
    c.drawRightString(70,100,"PHONE No. :")

    # This Block Consist of Item Description
    c.roundRect(15,108,170,130,10,stroke=1,fill=0)
    c.line(15,120,185,120)
    c.drawCentredString(25,118,"SR No.")
    c.drawCentredString(75,118,"GOODS DESCRIPTION")
    c.drawCentredString(125,118,"RATE")
    c.drawCentredString(148,118,"QTY")
    c.drawCentredString(173,118,"TOTAL")
    # Drawing table for Item Description
    c.line(15,210,185,210)
    c.line(35,108,35,220)
    c.line(115,108,115,220)
    c.line(135,108,135,220)
    c.line(160,108,160,220)

    # Declaration and Signature
    c.line(15,220,185,220)
    c.line(100,220,100,238)
    c.drawString(20,225,"We declare that above mentioned")
    c.drawString(20,230,"information is true.")
    c.drawString(20,235,"(This is system generated invoive)")
    c.drawRightString(180,235,"Authorised Signatory")

    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()
    print("invoice created")


# for generating pdf invoice
from extraPackage.invoice import render_to_pdf,genrate_invoice_pdf
from extraPackage.mailer import send_mail
import os
# def fetch_resources(uri, rel):
#     path = os.path.join(uri.replace(settings.STATIC_URL, ""))
#     return path

# sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
def genrate_invoice(request,slug):
    user = request.user
    order = Checkout.objects.get(order_id=slug,customer_user=user)
    template = 'payment/invoice.html'
    data = {
                'shop':latestSite,
                'checkout': order,
            }
    return genrate_invoice_pdf(template,data)

import uuid
from selling_product.models import CheckoutItemOwner
def orderPlace(request):
    if(request.method == "POST"):
        color = ""
        pid = int(request.POST['product_id'])
        qty = int(request.POST['quantity'])
        address_id = int(request.POST['address_id'])
        payment = request.POST['payment']
        address = BillingInfo.objects.get(id=address_id)
        product = Product.objects.get(id=pid)
        shipping_charge=product.shipping_charge
        tax = product.tax*qty
        total_amt = (product.price*qty)+tax+product.shipping_charge
        user = request.user
        available_product = product.available_product
        if(qty <= available_product ):
            # print(request.POST)
            for i in range(1,qty+1):
                color+=request.POST['p-color-'+str(i)]+","
            transaction_id = uuid.uuid1()
            Checkout(transaction_id=transaction_id,product=product,customer_user=user,billing_address=address,quantity=qty,tax=tax,color=color,total_amount=total_amt,delevery_charge=shipping_charge,delevery_mode=payment).save()
            Product.objects.filter(id=pid).update(available_product=(available_product-qty))
            # Do mail to customer and send him/her reciept for confirming their order
            # Make an invoice
            # invoice()
            order = Checkout.objects.get(transaction_id=transaction_id,customer_user=user)
            CheckoutItemOwner(checkout=order,product=product,item_owner=product.customer_user).save()
            template = 'payment/invoice.html'
            data = {
                'shop':latestSite,
                'checkout': order,
                'user':request.user
            }
            ## For GENRATE INVOICE
            send_mail(template,data)

            messages.success(request,"Your Order Placed ! <strong><a href='/dashboard/dashMyOrder' style='color:orange;'>Track Order & Get Invoice !</a></strong>")
            return redirect("/checkout/"+str(pid))
        else:
            return HttpResponse("Forbidden")
    else:
        return HttpResponse("Forbidden")

def about(request):
    about = AboutSite.objects.filter(site=latestSite).last()
    try:root_users = User.objects.all().order_by("id")[:4]
    except Exception:root_users = User.objects.all().order_by("id")[:2]
    except Exception:root_users = User.objects.all().order_by("id")[:1]
    except Exception:root_users = User.objects.all().order_by("id")
    try:usr_feedback = UserFeedback.objects.all().select_related("user","site").order_by('id')[:5]
    except Exception: usr_feedback = UserFeedback.objects.all().select_related("user","site").order_by('id')

    return render(request,"about.html",{
            'site_info_data':site_info_data,
            'about_site':about,
            'usr_feedback':usr_feedback,
            'root_users':root_users,'product_meta_data':meta_data()
            })

def contact(request):
    site_data = site_info_data
    if request.method == "POST":
        nm =  dataValidate((request.POST['name']))
        eml = dataValidate((request.POST['email']))
        sub = dataValidate((request.POST['subject']))
        msg = dataValidate((request.POST['message']))
        have_already = ContactUs.objects.filter(email=eml).count()
        if have_already == 0:
            ContactUs(name=nm,email=eml).save()
            cu_obj = ContactUs.objects.get(email=eml)
            ContactUsInfo(contact_us=cu_obj,subject=sub,message=msg).save()
        else:
            cu_obj = ContactUs.objects.get(email=eml)
            ContactUsInfo(contact_us=cu_obj,subject=sub,message=msg).save()
            
        messages.success(request,"You have successfully sent message to admin ! ")
        return redirect("/contact/")
    else:
        return render(request,"contact.html",{
            'site_info_data':site_info_data,
            'site_data':site_data,'product_meta_data':meta_data()
            })

def pnf404(request):
    site_data = site_info_data
    return render(request,"404.html",{
        'site_info_data':site_info_data,
        'site_data':site_data,
        'product_meta_data':meta_data()})

def faq(request):
    title_of_faq = TitleOfFaq.objects.filter(site=latestSite).last()
    faq = Faq.objects.filter(site=latestSite)
    return render(request,"faq.html",{
        'site_info_data':site_info_data,
        'title_of_faq':title_of_faq,
        'faq':faq,'product_meta_data':meta_data()
    })

def cart(request):
    return render(request,"cart.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def emptyBlog(request):
    site_data = site_info_data
    return render(request,"empty-blog-search.html",{
        'site_info_data':site_info_data,
        'site_data':site_data,
        'product_meta_data':meta_data()})


# def emptyWishlist(request):
#     return render(request,"empty-wishlist.html",{'site_info_data':site_info_data})

def emptySearch(request):
    site_data = site_info_data
    return render(request,"empty-search.html",{'site_info_data':site_info_data,'site_data':site_data,'product_meta_data':meta_data()})

def removeTag(request):
    if request.method == 'POST':
        tag=request.POST['tag']
        pid=request.POST['pid']
        uid=request.POST['uid']
        dataset = Product.objects.filter(id=pid,customer_user=uid)
        newTag = ''
        split_tag=[]
        for d in dataset:
            split_tag = str(d.tags).split(',')

        
        counter = 1
        for db_tag in split_tag:
            if tag.strip() != db_tag.strip():
                newTag+=db_tag.strip()
                newTag+=','
            counter+=1

        # LET'S CREATE FRESH TAGDATA
        fresh_tag=''
        for fresh in newTag.split(","):
            if fresh != '':
                fresh_tag+=fresh
                fresh_tag+=','
        Product.objects.filter(id=pid,customer_user=uid).update(tags=fresh_tag)

        # # DATA UPDATING IN TAG TABLE
        product = Product.objects.get(id=pid)
        user = User.objects.get(id=uid)
        tags = newTag.split(",")
        ProductTags.objects.filter(user=uid,product=pid).delete()
        for newTg in tags:
            if newTg != '':
                ProductTags(user=user,product=product,tag=newTg).save()
        return HttpResponse("updated")
    else:
        return HttpResponse("invalid user")

# ADD NEW TAG
def addNewTag(request):
    if request.method == "POST":
        uid = request.POST['uid']
        pid = request.POST['pid']
        new_tags = request.POST['new-tag']

        # FIRST OF ALL WE HAVE TO FETCH ALL TAGS FROM DATABASE
        db_tags = Product.objects.filter(id=pid,customer_user=uid)
        new_created_tags = ''
        for tg in db_tags:
            new_created_tags+=tg.tags
            if len(tg.tags)>0 and tg.tags[-1] != ',': # CHECK ANY TAGS AVAILABLE AND END OF TAG STORED COMMAN (,)
                new_created_tags+=","
            new_created_tags+=new_tags
            
        splited_tags = new_tags.split(",")
        usr = User.objects.get(id=uid)
        pd = Product.objects.get(id=pid)
        for tag in splited_tags:
            if tag != '':
                ProductTags(user=usr,product=pd,tag=tag).save()
        Product.objects.filter(customer_user=uid,id=pid).update(tags=new_created_tags)
        return HttpResponse("updated")
    else:
        return HttpResponse("invalid user")

# REVIEW ADDING FOR USER
def addNewReview(request):
    if request.method=='POST':
        rate = int(request.POST['rating'])
        uid = request.POST['user-id']
        pid = request.POST['product-id']
        review_text = dataValidate(request.POST['review-text'])
        user = User.objects.get(id=uid)
        product = Product.objects.get(id=pid)
        # SET AVERAGE OF PRODUCT RATING
        ProductReview(product=product,customer_user=user,review_rating=rate,review_comment=review_text).save()
        Product.objects.filter(id=pid).update(average_rating=Rating().rating_avg(pid))
        return redirect("/productDetails/"+str(pid)+"?#pd-tag")
    else:
        return HttpResponse('Forbidden')

# REVIEW REMOVING FUNCTION
def removeReview(request):
    if request.method=='POST':
        review_id = request.POST['review_id']
        uid = request.POST['uid']
        pid = request.POST['pid']
        ProductReview.objects.filter(id=review_id,customer_user=uid,product=pid).delete()
        return HttpResponse("deleted")
    else:
        return HttpResponse("invalid")

def voteForReview(request):
    if request.method=='POST':
        review_id = request.POST['review-id']
        product_id = request.POST['product-id']
        user_id = request.POST['user-id']
        tag = request.POST['tag']
        action = request.POST['action']
        user=User.objects.get(id=user_id)
        product=Product.objects.get(id=product_id)
        review=ProductReview.objects.get(id=review_id)
        if tag=='upvote' and action=='add':
            ReviewVote.objects.filter(review=review_id,customer_user=user_id,product=product_id).delete()
            ReviewVote(product=product,customer_user=user,review=review,is_up_vote=True).save()
        elif tag=='upvote' and action=='remove':
            ReviewVote.objects.filter(review=review_id,customer_user=user_id,product=product_id).delete()
        elif tag=='downvote' and action=='add':
            ReviewVote.objects.filter(review=review_id,customer_user=user_id,product=product_id).delete()
            ReviewVote(product=product,customer_user=user,review=review,is_up_vote=False).save()
        elif tag=='downvote' and action=='remove':
            ReviewVote.objects.filter(product=user_id,customer_user=user_id,review=review_id).delete()

        upVote=ReviewVote.objects.filter(product=product_id,review=review_id,is_up_vote=True).count()
        downVote=ReviewVote.objects.filter(product=product_id,review=review_id,is_up_vote=False).count()
        return HttpResponse(str(upVote)+"-"+str(downVote))
    else:
        return HttpResponse("invalid-user")

# REVIEW UPDATING
def updateReview(request):
    if request.method=='POST':
        rate = int(request.POST['rating'])
        uid = request.POST['user-id']
        pid = request.POST['product-id']
        review_text = dataValidate(request.POST['review-text'])
        ProductReview.objects.filter(product=pid,customer_user=uid).update(review_rating=rate,review_comment=review_text)
        Product.objects.filter(id=pid).update(average_rating=Rating().rating_avg(pid))
        # print("updated")
        return redirect("/productDetails/"+str(pid)+"?#pd-tag")
    else:
        return HttpResponse("Forbidden")

# REVIEW SORTING
def sortReview(request):
    if request.method=='POST':
        sortBy = request.POST['sort-by']
        uid = int(request.POST['uid'])
        pid = int(request.POST['pid'])
        user = User.objects.get(id=uid)
        product = Product.objects.get(id=pid)
        reviews = ProductReview.objects.filter(product=pid).order_by(sortBy)
        return render(request,'request_data/sorted-review-data.html',{'user':user,'product':product,'reviews':reviews})
    else:
        return HttpResponse("Forbidden")
        
def fetchMoreReview(request):
    pid = request.GET['pid']
    uid=request.GET['uid']
    start_limit = int(request.GET['start'])
    end_limit = int(request.GET['end'])
    is_sort = request.GET['is-sorted-data']
    if is_sort=='':
        reviews = ProductReview.objects.filter(product=pid).order_by("-review_rating")[start_limit:end_limit]
    else:
        reviews = ProductReview.objects.filter(product=pid).order_by(is_sort)[start_limit:end_limit]
    product = Product.objects.get(id=pid)
    user = User.objects.get(id=uid)
    return render(request,'request_data/sorted-review-data.html',{'user':user,'product':product,'reviews':reviews})

def setHostnameIP(request):
    if request.method=='POST':
        def add_product_view_counter(product,tvObj,product_id):
                # IF NO VIEWS AVALABLE, THEN NEW DATA SAVING
            # print("New Views Detected")
            if tvObj.count() != 0:
                # IF VIEWS AVALABLE, THEN ADD 1 MORE VIEW INTO VIEWS FIELD
                TotalViews.objects.filter(product=product_id).update(views=int(tvObj.views)+1)
                # print("value increased")
            else:
                # IF NO VIEWS AVALABLE, THEN NEW DATA SAVING
                # print("value saved")
                TotalViews(product=product,views=1).save()
                
        product_id = request.POST['product-id']
        user_id = request.POST['user-id']
        data = request.POST['hostname-ip'].split(",")
        hostname=data[0]
        ip=data[1]
        product=Product.objects.get(id=product_id)
        tvObj = TotalViews.objects.filter(product=product_id)
        # print("host name =>"+hostname)
        # print("host IP =>"+ip)
        # IF USER LOGGIN THEN ADD DATA INTO VALID USER FIELD 
        if user_id != '':
            user = User.objects.get(id=user_id)
            if ProductUserViews.objects.filter(product=product_id,user=user_id).count() == 0:
                ProductUserViews(product=product,user=user,host_name=hostname,host_ip=ip).save()
                add_product_view_counter(product,tvObj,product_id)
        else:
            if ProductViews.objects.filter(product=product_id,host_name=hostname,host_ip=ip).count() == 0:
                ProductViews(product=product,host_name=hostname,host_ip=ip).save()
                add_product_view_counter(product,tvObj,product_id)

        return HttpResponse("Viewed")
    else:
        return HttpResponse("Forbidden")

def res():
    return HttpResponse("Forbidden")


# REVIEW GETTING ONE BY ONE 
def fetchMoreNewArrivalProduct(request):
    if request.method=='POST':
        start = int(request.POST['start'])
        end = int(request.POST['end'])
        shop_name=request.POST['shop-name']
        order_by=request.POST['order-by']
        query=request.POST['query']
        if request.user.is_authenticated:
            # IF LOGGED USER REQUESTED BEST PRODUCT PREDICTING ALGO -> from extraPackage.productAlgo import loggedUser(user_id)
            # products = ArrivalProduct(order_by).loggedUser(request.user.id)
            if query == '' or query == None:
                products = Product.objects.all().order_by(order_by)[start:end]
            else:
                products = Product.objects.filter(Q(tags__contains=query) or Q(discription__contains=query) or Q(price__contains=query or Q(m_r_p__contains=query) or Q(discount_percentage__contains=query) or Q(extra_info__contains=query) or Q(title__contains=query))).order_by(order_by)[start:end]
                if products.count() == 0:
                    return render(request,'request_data/empty-query.html')
            return render(request,'request_data/new-arrival-product.html',{'user':request.user,'products':products,'shop_name':shop_name})
            
        elif not request.user.is_authenticated:
            # IF LOGGED USER REQUESTED BEST PRODUCT PREDICTING ALGO -> from extraPackage.productAlgo import anonymousUser(host_name,host_ip)
            # data = request.POST['is-user'].split(",")
            # hostname=data[0]
            # ip=data[1]
            # products = ArrivalProduct(order_by).anonymousUser(hostname,ip)    
            if query == '' or query == None:
                products = Product.objects.all().order_by(order_by)[start:end]
            else:        
                products = Product.objects.filter(Q(tags__contains=query) or Q(discription__contains=query) or Q(price__contains=query or Q(m_r_p__contains=query) or Q(discount_percentage__contains=query) or Q(extra_info__contains=query) or Q(title__contains=query))).order_by(order_by)[start:end]
                if products.count() == 0:
                    return render(request,'request_data/empty-query.html')
            return render(request,'request_data/new-arrival-product.html',{'user':request.user,'products':products,'shop_name':shop_name})

    else:
        return res()

def query(request):
    query = request.GET['query']
    queryList=query.split(",")
    # products = Product.objects.filter(tags__contains=query)
    products = Product.objects.filter(Q(tags__contains=query) or Q(discription__contains=query) or Q(price__contains=query or Q(m_r_p__contains=query) or Q(discount_percentage__contains=query) or Q(extra_info__contains=query) or Q(title__contains=query)))[0:20]
    if products.count() == 0:
        return render(request,'empty-search.html',{'site_info_data':site_info_data,'product_meta_data':meta_data()})
    # print(products)
    return render(request,'shop-list-left.html',{'site_info_data':site_info_data,
        'usr_query':queryList,
        'embed_query':query,
        'product_meta_data':meta_data(),'products':products
        })


def addMoreOrder(request):
    product = Product.objects.filter(id=request.GET['pid'])
    return render(request,'include/product/order.html',{'product':product,'counter':request.GET['p-counter']})

from extraPackage.mailer import cancel_order
def cancelOrder(request,slug):
    uid = request.user.id
    order_id = slug
    Checkout.objects.filter(order_id=order_id,customer_user=uid).update(order_status='cancel')
    data = {
    'checkout': slug,
    'user':request.user
    }
    cancel_order(data)

    # OrderTracking.objects.filter(tracking_id=order_id).update(status='cancel')
    return redirect("/dashboard/dashCancellation")

def returnOrder(request,slug):
    uid = request.user.id
    order_id = slug
    Checkout.objects.filter(order_id=order_id,customer_user=uid).update(order_status='return')
    return redirect("/dashboard/returned-order")
