# from accounts.models import User
from django.db.models.query_utils import Q

from EshopApp.views import checkout
from .models import Product, ProductBrand, ProductImage, ProductSubscriber, ProductTags, Subcategory, Wishlist
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from EshopApp.models import SiteInfo
from .productForm import ProductForm,ProductImageForm,ProductEditForm,ProductEditImageForm
from django.contrib import messages
from accounts.models import User
import math
from EshopApp.views import meta_data
# Create your views here.
import os
def productEdit(request,productId):
    site_info_data = SiteInfo.objects.last()
    product = Product.objects.get(id=productId)
    product_images = ProductImage.objects.filter(product=productId)
    product_form = ProductEditForm()
    product_img_form = ProductEditImageForm()
    product_images_form = ProductImageForm()
    if request.method == 'POST':
        instance = get_object_or_404(Product,id=productId)
        if request.FILES:
            form = ProductEditImageForm(request.POST, request.FILES,instance=instance)
            if form.is_valid():
                os.remove("media/%s"%(product.image))
                form.save()
                # print("valid form")
                messages.success(request,"Product Image Updated !")
                return redirect("/selling_product/productEdit/"+str(productId))
            else:
                # print("invalid form")
                messages.error(request,"Error : Invalid Form !")
                return redirect("/selling_product/productEdit/"+str(productId))
        else:
            form = ProductEditForm(request.POST,instance=instance)
            if form.is_valid():
                form.save()
                # print("valid form")
                product = Product.objects.get(id=productId)
                user = User.objects.get(id=request.user.id)
                tags = request.POST['tags'].split(",")
                ProductTags.objects.filter(user=request.user.id,product=productId).delete()
                for tag in tags:
                    if tag != '':
                        ProductTags(user=user,product=product,tag=tag).save()
                
                discount=math.floor((((product.m_r_p-product.price)/product.m_r_p)*100))
                Product.objects.filter(id=product.id).update(discount_percentage=discount)
                # print("discount => "+str(discount)+str(s))
                messages.success(request,"Product Infomation Updated !")
                return redirect("/selling_product/productEdit/"+str(productId))
            else:
                # print("invalid form")
                messages.error(request,"Error : Invalid Form !")
                return redirect("/selling_product/productEdit/"+str(productId))
    else:
        return render(request,'sell-product-edit.html',{
            'site_info_data':site_info_data,
            'product':product,
            'product_images':product_images,
            'product_form':product_form,
            'product_img_form':product_img_form,
            'product_images_form':product_images_form,
            'product_meta_data':meta_data()
            })

def selledProduct(request):
    product = Product.objects.all().order_by("-id")
    site_info_data = SiteInfo.objects.last()
    return render(request,'sell-product-index.html',{
        'site_info_data':site_info_data,
        'products':product,
        'product_meta_data':meta_data()})

def sellMoreProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            id=form.save()
            product = Product.objects.get(id=id.id)
            discount=math.floor((((id.m_r_p-id.price)/id.m_r_p)*100))
            Product.objects.filter(id=id.id).update(discount_percentage=discount)
            user = User.objects.get(id=request.POST['customer_user'])
            tags = request.POST['tags'].split(",")
            for tag in tags:
                if tag != '':
                    ProductTags(user=user,product=product,tag=tag).save()
            # print("OFFER END AT => "+request.POST['offer_end'])
            return redirect("/selling_product/add-product-img/"+str(id.id))
        else:
            messages.error(request,"Error : Invalid form..")
            return redirect("/selling_product/add-product-img/")
    else:
        product_form = ProductForm()
        site_info_data = SiteInfo.objects.last()
        return render(request,'sell-more-product.html',{
            'site_info_data':site_info_data,
            'product_form':product_form,
            'product_meta_data':meta_data()})

from .models import Checkout
from selling_product.models import CheckoutItemOwner
def topSells(request):
    site_info_data = SiteInfo.objects.last()
    uid = request.user.id
    owner_products = Product.objects.filter(customer_user=uid)
    checkouts=[]
    products = []
    sells = []
    for product in owner_products:
        cio=CheckoutItemOwner.objects.filter(item_owner=uid,product=product.id)
        if cio.count() != 0:
            products.append(product.title)
            checkouts.append(product)
            sum=0
            for total_sells in cio:
                sum+=Checkout.objects.get(id=total_sells.checkout.id).quantity
            sells.append(sum)
    print(checkouts)
    # print(sorted(checkouts))
    return render(request,'sell-top-sells.html',{'site_info_data':site_info_data,'product_meta_data':meta_data(),'sells':sells,'products':products,'checkouts':checkouts})

def holdDelevery(request):
    uid = request.user.id
    site_info_data = SiteInfo.objects.last()
    owner_products = Product.objects.filter(customer_user=uid)
    total_sells = owner_products.count()
    hold_delivery=0
    processing=0
    shipped=0
    deliverd=0
    cancel=0
    returns=0
    for product in owner_products:
        cio=CheckoutItemOwner.objects.filter(item_owner=uid,product=product.id)
        for sells in cio:
            prc = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='processing').count()
            ship = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='shipped').count()
            deli = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='delivered').count()
            canc = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='cancel').count()
            ret = Checkout.objects.filter(order_id=sells.checkout.order_id,order_status='return').count()
            if(prc != 0):
                processing+=1
            if(ship != 0):
                shipped+=1
            if(deli != 0):
                deliverd+=1
            if(canc != 0):
                cancel+=1
            if(ret != 0):
                returns+=1

    return render(request,'sell-hold-delevery.html',{'site_info_data':site_info_data,'product_meta_data':meta_data(),'process':processing,'shipped':shipped,'deliverd':deliverd,'cancel':cancel,'returns':returns,'total_sells':total_sells,'hold_delivery':hold_delivery})
    
site_info_data = SiteInfo.objects.last()
def deleverdProduct(request):
    uid = request.user.id
    owner_products = Product.objects.filter(customer_user=uid)
    deliveries = []
    for product in owner_products:
        checkout = Checkout.objects.filter(product=product.id,order_status='delivered')
        deliveries.extend(list(checkout))

    return render(request,'sell-deleverd-product.html',{'site_info_data':site_info_data,'product_meta_data':meta_data(),'deliveries':deliveries})

def returnsProduct(request):
    uid = request.user.id
    owner_products = Product.objects.filter(customer_user=uid)
    checkouts = []
    deliverd = []
    for product in owner_products:
        checkout = Checkout.objects.filter(product=product.id,order_status='return')
        deliverd.extend(list(Checkout.objects.filter(product=product.id,order_status='delivered')))
        checkouts.extend(list(checkout))
    return render(request,'sell-returns-product.html',{'site_info_data':site_info_data,'product_meta_data':meta_data(),'checkouts':checkouts,'deliverd':deliverd})
from django.db.models import Count
def clientList(request):
    checkouts = CheckoutItemOwner.objects.filter(item_owner=request.user.id)
    clients = []
    client_id = []
    for checkout in checkouts:
        order = Checkout.objects.filter(product=checkout.product)
        if order[0].customer_user.id not in client_id:
            clients.extend(list(order))
            client_id.append(order[0].customer_user.id)

            # client_id.append()
    return render(request,'sell-client-list.html',{'product_meta_data':meta_data(),'site_info_data':site_info_data,'clients':clients})

def dropdown(request):
    if request.method == 'GET':
        if(request.GET['type']=='subcategory'):
            pk = request.GET['id']
            subcategory = Subcategory.objects.filter(product_categories=pk)
            return render(request,'chaning_dropdown/subcategory.html',{'subcategory':subcategory})
        else:
            pk = request.GET['id']
            brand = ProductBrand.objects.filter(category=pk)
            return render(request,'chaning_dropdown/brand.html',{'brand':brand})

# THIS IS FOR REDIRECTING IN ADDING IMAGE PAGE
def addProductImage(request,reqID):
    id = int(reqID)
    form = ProductImageForm()
    site_info_data = SiteInfo.objects.last()
    images = ProductImage.objects.filter(product=id).order_by('id')
    if request.method == "POST":
        ourform = ProductImageForm(request.POST,request.FILES)
        if ourform.is_valid():
            ourform.save()
            return redirect("/selling_product/add-product-img/"+str(id))
        else:
            return HttpResponse("Invalid Form")
            # print("Invalid Form")
    else:
        return render(request,'sell-product-image.html',{
                'product_id':id,
                'form':form,
                'site_info_data':site_info_data,
                'images':images,'product_meta_data':meta_data()
            })
            
# THIS IS FOR REDIRECTING IN EDIT PAGE
def addProductImages(request,reqID):
    id = int(reqID)
    form = ProductImageForm()
    site_info_data = SiteInfo.objects.last()
    images = ProductImage.objects.filter(product=id).order_by('id')
    if request.method == "POST":
        ourform = ProductImageForm(request.POST,request.FILES)
        if ourform.is_valid():
            ourform.save()
            return redirect("/selling_product/productEdit/"+str(id))
        else:
            return HttpResponse("Invalid Form")
            # print("Invalid Form")
    else:
        return render(request,'sell-product-image.html',{
                'product_id':id,
                'form':form,
                'site_info_data':site_info_data,
                'images':images,'product_meta_data':meta_data()
            })


# search product by id
def getProductById(request):
    if request.method == 'GET':
        pid = request.GET['productId']
        loggedUser = request.GET['loggedUser']
        filterBy = request.GET['filterBy']
        if pid == '' or pid == None:
            try:products = Product.objects.filter(customer_user=loggedUser)
            except:products=False
        else:
            if filterBy == 'id':
                try:products = Product.objects.filter(id=pid, customer_user=loggedUser)
                except: products = False

            elif filterBy == 'add_date_time':
                try:products = Product.objects.filter(add_date_time__contains=pid, customer_user=loggedUser)
                except: products = False

            elif filterBy == 'name':
                try:products = Product.objects.filter(title__contains=pid, customer_user=loggedUser)
                except: products = False

            elif filterBy == 'price':
                print(filterBy)
                try:products = Product.objects.filter(price__contains=pid, customer_user=loggedUser)
                except: products = False

            elif filterBy == 'color_code':
                try:products = Product.objects.filter(color_code__contains=pid, customer_user=loggedUser)
                except: products = False
                
            elif filterBy == 'size':
                try:products = Product.objects.filter(size__contains=pid, customer_user=loggedUser)
                except: products = False

            elif filterBy == 'weight':
                try:products = Product.objects.filter(weight__contains=pid, customer_user=loggedUser)
                except: products = False
        return render(request,"request_data/product-filter-by-id.html",{'products':products})


def deleteImages(request):
    if request.method == 'POST':
        image_id = request.POST['image-id']
        product_id = request.POST['product-id']
        image=ProductImage.objects.get(id=image_id)
        os.remove("media/%s"%(image.img_path))
        ProductImage.objects.filter(id=image_id,product=product_id).delete()
        return HttpResponse("Deleted")
    else:
        return HttpResponse("invalid user")

# DELETING ENTIRE PRODUCT
def deleteProduct(request):
    if request.method=='POST':
        p_id = request.POST['product-id']
        Product.objects.filter(id=p_id).delete()
        return HttpResponse("Deleted")
    else:
        return HttpResponse("invalid User")


# FETCHING SINGLE PRODUCT
def getOneProduct(request):
    if request.method=='GET':
        id = request.GET['product-id']
        shop = request.GET['shop']
        product = Product.objects.get(id=id)
        return render(request,"request_data/quick-look-modal.html",{'shop':shop,'product':product})
    else:
        return HttpResponse("Invalid user")

# FETCHING CART PRODUCT
def getCartProduct(request):
    if request.method=='GET':
        id = request.GET['product-id']
        quantity = request.GET['quantity']
        items = request.GET['total-item']
        product = Product.objects.get(id=id)
        return render(request,"request_data/cart-modal.html",{'product':product,'quantity':quantity,'items':items})
    else:
        return HttpResponse("Invalid user")

def getProducts(request):
    if request.method=='GET':
        site_info_data = SiteInfo.objects.last()
        product_id = request.GET['product-id']
        quantity = request.GET['quantity']
        request_from = request.GET['from']
        product = Product.objects.get(id=product_id)
        if request_from == 'cart-page':
            return render(request,'request_data/cart-page-items.html',{'product':product,'quantity':quantity,'site_info_data':site_info_data})
        else:
            return render(request,'request_data/cart-items.html',{'product':product,'quantity':quantity,'site_info_data':site_info_data})
            
    else:
        # return HttpResponse("invalid user")
        print("invalid user")
    
def addMywishlist(request):
    if request.method=='POST':
        user = request.POST['user']
        product = request.POST['product']
        status = request.POST['status']
        if str(status) == 'true':
            status = True
            user = User.objects.get(id=request.user.id)
            product = Product.objects.get(id=product)
            res = Wishlist(customer_user=user,product=product)
            res.save()
            # print(product)
            return HttpResponse("Added")
        else:
            Wishlist.objects.filter(customer_user=request.user.id,product=product).delete()
            # print(product)
            return HttpResponse("Removed")
    else:
        return HttpResponse("invalid user")

# Clearing all wishlist
def clearMyWishlist(request):
    if request.method=='POST':
        user = request.POST['user_id']
        Wishlist.objects.filter(customer_user=user).delete()
        return HttpResponse("Wishlist cleared")
    else:
        return HttpResponse("invalid user")

def removeWishlist(request):
    if request.method=='POST':
        Wishlist.objects.filter(id=request.POST['wishlist-id']).delete()
        return HttpResponse("Removed")
    else:
        return HttpResponse("invalid user")

def addProductSubscriber(request):
    if request.method=='POST':
        user = request.POST['user']
        product = request.POST['product']
        status = request.POST['status']
        if str(status) == 'true':
            status = True
            user = User.objects.get(id=user)
            product = Product.objects.get(id=product)
            res = ProductSubscriber(user=user,product=product)
            res.save()
            # print(product)
            return HttpResponse("Added")
        else:
            ProductSubscriber.objects.filter(user=user,product=product).delete()
            # print(product)
            return HttpResponse("Removed")
    else:
        return HttpResponse("invalid user")

from extraPackage.mailer import order_action
def orderAction(request):
    if request.method == "POST":
        # print(request.POST)
        action = request.POST['action']
        checkout_id = int(request.POST['cid'])

        Checkout.objects.filter(id=checkout_id).update(order_status=action)
        checkout = Checkout.objects.filter(id=checkout_id)
        data={
            'action':action,
            'checkout':checkout,
            'email':request.user.email
        }
        order_action(data)
        # Do mail to user your data status

        return HttpResponse("success")
    else:
        return HttpResponse("Forbidden")

def viewCheckout(request):
    if request.method == "POST":
        checkout = Checkout.objects.get(id=int(request.POST['cid']))
        return render(request,"request_data/checkout/checkout-details.html",{'checkout':checkout})
    else:
        return HttpResponse("Forbidden")

def viewClient(request):
    if request.method == "POST":
        # print("")
        # print("")
        # print("")
        # print("")
        # print("")
        # print("")
        # print("")
        # print("")
        # print(request.POST)
        checkouts = CheckoutItemOwner.objects.filter(item_owner=request.user.id)
        client = []
        client_detail = []
        checkout_details = []
        client_id = []
        for checkout in checkouts:
            print(checkout.id)
            order = Checkout.objects.filter(product=checkout.product.id,customer_user=int(request.POST['client']))
            client_detail.append(list(order))
            order_last = client_detail[0]
            if order_last[0].customer_user.id not in client_id:
                client.append(order_last[0])
                client_id.append(order_last[0].customer_user.id)
            else:
                checkout_details.extend(list(order))

        return render(request,"request_data/checkout/client-details.html",{'checkouts':client,'checkout_detail':checkout_details})
    else:
        return HttpResponse("Forbidden")

