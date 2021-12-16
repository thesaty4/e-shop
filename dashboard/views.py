from selling_product.models import Checkout
from accounts.models import BillingInfo
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from EshopApp.models import SiteInfo
from .dashForm import UserInfo,UpdateProfilePic,BillingInfoFrom
from extraPackage.auth import dataValidate
from accounts.models import User
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
# from validate_email import validate_email
from EshopApp.views import meta_data
site_info_data = SiteInfo.objects.last()
# Create your views here.
def dashboard(request):
    try:billing_info = BillingInfo.objects.all()
    except BillingInfo.DoesNotExist:billing_info=False
    return render(request,"dashboard.html",{'site_info_data':site_info_data,'billing_info':billing_info,'product_meta_data':meta_data()})

def dashMyProfile(request):
    return render(request,"dash-my-profile.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def dashAddressBook(request):
    try:billing_info = BillingInfo.objects.all()
    except BillingInfo.DoesNotExist:billing_info=False
    return render(request,"dash-address-book.html",{'site_info_data':site_info_data,'billing_info':billing_info,'product_meta_data':meta_data()})

def dashTrackOrder(request):
    return render(request,"dash-track-order.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def dashMyOrder(request):
    return render(request,"dash-my-order.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def dashPaymentOption(request):
    return render(request,"dash-payment-option.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def dashCancellation(request):
    return render(request,"dash-cancellation.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})
def dashReturning(request):
    return render(request,"dash-returning.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def dashEditProfile(request):
    userInfo = UserInfo()
    profilePicForm = UpdateProfilePic()
    return render(request,"dash-edit-profile.html",
    {
        'site_info_data':site_info_data,
        'userInfo':userInfo,
        'profilePicForm':profilePicForm,
        'product_meta_data':meta_data()
    })

def dashManageOrder(request,order_id):
    try:
        order = Checkout.objects.get(order_id=order_id) 
        return render(request,"dash-track-order.html",{'site_info_data':site_info_data,'product_meta_data':meta_data(),'tracking_order':order})
    except:  
        return render(request,"dash-track-order.html",{'site_info_data':site_info_data,'product_meta_data':meta_data(),'invalid_order':'yes'})

def dashAddMakeDefault(request):
    if request.method == 'POST':
        userId = request.POST['userId']
        address = request.POST['addressId']
        status = BillingInfo.objects.filter(id=address,is_shipping_details=False)
        if(status.count()):
            BillingInfo.objects.filter(user=userId).update(is_shipping_details=False)
            BillingInfo.objects.filter(id=address).update(is_shipping_details=True)
            return HttpResponse("valid")
        else:
            return HttpResponse("invalid")
    else:
        try:billing_info = BillingInfo.objects.all()
        except BillingInfo.DoesNotExist:billing_info=False
        return render(request,"dash-address-make-default.html",{'site_info_data':site_info_data,'billing_info':billing_info,'product_meta_data':meta_data()})

def dashAddressAdd(request):
    if request.method=='POST':
        loggedUser = User.objects.get(id=request.POST['loggedUser'])
        fname = dataValidate(request.POST['fname']).upper()
        lname = dataValidate(request.POST['lname']).upper()
        phone = request.POST['phone']
        country = dataValidate(request.POST['country'])
        state = dataValidate(request.POST['state'])
        zip = dataValidate(request.POST['zip'])
        address = dataValidate(request.POST['address']).upper()
        status = BillingInfo.objects.filter(user=loggedUser)
        if status.count():
            infoStatus = BillingInfo(user=loggedUser,first_name=fname,last_name=lname,mobile=phone,country=country,state=state,pin_code=zip,full_address=address,is_shipping_details=False,is_billing_details=False)
            infoStatus.save()
            return HttpResponse("success")
        else:
            infoStatus1 = BillingInfo(user=loggedUser,first_name=fname,last_name=lname,mobile=phone,country=country,state=state,pin_code=zip,full_address=address)
            infoStatus1.save()
            return HttpResponse("success")
    else:
        address_form = BillingInfoFrom()
        return render(request,"dash-address-add.html",{'site_info_data':site_info_data,'address_form':address_form,'product_meta_data':meta_data()})

def dashAddressEdit(request,addressId: int):
    if request.method=='POST':
        loggedUser = dataValidate(request.POST['loggedUser'])
        fname = dataValidate(request.POST['fname']).upper()
        lname = dataValidate(request.POST['lname']).upper()
        phone = request.POST['phone']
        country = dataValidate(request.POST['country'])
        state = dataValidate(request.POST['state'])
        zip = dataValidate(request.POST['zip'])
        address = dataValidate(request.POST['address']).upper()
        BillingInfo.objects.filter(id=addressId,user=loggedUser).update(first_name=fname,last_name=lname,mobile=phone,country=country,state=state,pin_code=zip,full_address=address)
        return HttpResponse("success")
    else:
        shipping_address = BillingInfo.objects.get(id=addressId)        
        shipping_form = BillingInfoFrom()
        return render(request,"dash-address-edit.html",{
            'site_info_data':site_info_data,
            'shipping_address':shipping_address,
            'shipping_form':shipping_form,
            'product_meta_data':meta_data()
            })

def dashChangePass(request):
    return render(request,"dash-change-password.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def usernameExists(uname):
    try:
        User.objects.get(username=uname)
        return True
    except User.DoesNotExist:
        return False

def emailExists(mail):
    try:
        User.objects.get(email=mail)
        return True
    except User.DoesNotExist:
        return False

# UPDATING USER CREDENTIAL
def profileUpdate(request):
    if request.method=="POST":
        loggedUserId = dataValidate(request.POST['loggedUserId'])
        uname = dataValidate(request.POST['username'])
        email = dataValidate(request.POST['email'])
        fname = dataValidate(request.POST['fname'])
        lname = dataValidate(request.POST['lname'])
        gender = dataValidate(request.POST['gender']).upper()
        dob = request.POST['dob']
        country = dataValidate(request.POST['country']).upper()
        if(usernameExists(uname)):
            # USERNAME IS NOT UPDATE
            if(emailExists(email)):
                # EMAIL IS NOT UPDATE NOR USERNAME
                User.objects.filter(id=loggedUserId).update(first_name=fname,last_name=lname,gender=gender,dob=dob,country=country)
                return HttpResponse("updated")
            else:
                # UPDATE DATA WITH EMAIL BUT NOT WITH USERNAME
                User.objects.filter(id=loggedUserId).update(email=email,first_name=fname,last_name=lname,gender=gender,dob=dob,country=country)
                print("updated")
                return HttpResponse("updated")
        else:
            # DATA WILL UPDATE WITH USERNAME
            if(emailExists(email)):
                # EMAIL IS NOT UPDATE NOR USERNAME
                User.objects.filter(id=loggedUserId).update(username=uname,first_name=fname,last_name=lname,gender=gender,dob=dob,country=country)
                print("updated")
                return HttpResponse("updated")

            else:
                # UPDATE DATA WITH EMAIL WITH USERNAME   
                User.objects.filter(id=loggedUserId).update(username=uname,email=email,first_name=fname,last_name=lname,gender=gender,dob=dob,country=country)
                print("updated")
                return HttpResponse("updated")
            
    else:
        return HttpResponse("Forbidden")

# UPDATING USER PROFILE PIC
import os
def updateProfilePic(request):
    if request.method=="POST":
        instance = get_object_or_404(User, id=request.POST['loggedUserId'])
        form = UpdateProfilePic(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            # User.objects.filter(id=dataValidate(request.POST['loggedUserId'])).update(profile_pic=form.save())
            # print(request.user.profile_pic)
            os.remove("media/%s"%(request.user.profile_pic))
            form.save()
            return redirect("/dashboard/dashEditProfile/")
        else:
            return redirect("/dashboard/dashEditProfile/")
    else:
        return redirect("/")


# PASSWORD VERIFYING
def verifyPassword(request):
    if request.method=='POST':
        loggedUser = request.POST['loggedUser']
        password = request.POST['password']
        usr = auth.authenticate(username=loggedUser,password=password)
        if usr is not None:
            return HttpResponse('valid')
        else:
            return HttpResponse('invalid')
    else:
        return redirect("/")


def changePassword(request):
    if request.method=='POST':
        loggedUser = request.POST["loggedUser"]
        oldPassword = request.POST['oldPassword']
        newPassword = make_password(request.POST['newPassword'])
        status = auth.authenticate(username=loggedUser,password=oldPassword)
        if status is not None:
            User.objects.filter(username=loggedUser).update(password=newPassword)
            auth.login(request,status)
            return HttpResponse("updated")
            # usr = auth.authenticate(username=loggedUser,password=newPassword)
            # if usr is not None:
                # auth.login(request,usr)
                # return redirect("/dashboard/dash-change-password/")
            # else:
            #     return redirect("/")
        else:
            return HttpResponse("notUpdated")
    else:
        return redirect("/")

def deleteAddress(request):
    if request.method == 'POST':
        addressId = request.POST['addressId']
        userId = request.POST['userId']
        usr = User.objects.get(id=userId)
        if usr:
            data=BillingInfo.objects.get(id=addressId)
            data.delete()
            return HttpResponse("")
    else:
        return redirect("/")

def myOrderSort(request):
    uid = request.user.id
    if(request.GET['qty'] == 'all'):
        order = Checkout.objects.filter(customer_user=uid).order_by("-id")
    else:
        qty = int(request.GET['qty'])
        order = Checkout.objects.filter(customer_user=uid).order_by("-id")[:qty]
    return render(request,"request_data/my-order-sort.html",{'our_orders':order})