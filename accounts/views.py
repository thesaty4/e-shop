# // @Author SATYA NARAYAN MISHRA
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import User
from EshopApp.models import SiteInfo
from extraPackage.auth import dataValidate
from django.contrib.auth.hashers import check_password,make_password
from .myForms import Customer_reg_form
from EshopApp.views import meta_data
# from .models import User
# from verify_email import verify_email
from validate_email import validate_email
site_info_data = SiteInfo.objects.last()
latestSite = SiteInfo.objects.last()

# Create your views here.


####################### Username validation ########################### 
def validate_my_username(request):
    username= dataValidate(request.POST['user_name'])
    status = User.objects.filter(username=username)
    if status.count() == 0:
        return HttpResponse("valid")
    else:
        return HttpResponse("invalid")

####################### Email validation ########################### 
def validate_my_email(request):
    mail = dataValidate(request.POST['email']).lower()
    if validate_email(mail):
        status = User.objects.filter(email=mail)
        if status.count() == 0:
            return HttpResponse("valid")
        else:
            return HttpResponse("invalid")
    else:
        return HttpResponse("invalid email")

####################### cropMyProfile ##############################
def cropMyProfile(request):
    request.POST = request.POST.copy()
    simple_pass = request.POST['password'].strip()
    has_password = make_password(simple_pass)
    request.POST['password']=has_password

    form = Customer_reg_form(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request,"Account has been created !")
        return redirect("/accounts/register/")
    else:
        messages.success(request,"Invalid Credantial")
        return redirect("/accounts/register/")

def register(request):
    if request.method == "POST":
        try:usr=request.POST['username_validation']
        except Exception:usr = False
        try:mail=request.POST['email_validation']
        except Exception:mail = False
        try:regProfileCropper=request.POST['password']
        except Exception:regProfileCropper= False
        if usr:
            return validate_my_username(request)
        elif mail:
            print(request.POST['email_validation'])
            return validate_my_email(request)
        elif regProfileCropper:
            return cropMyProfile(request)
    else:
        reg_form = Customer_reg_form()
        return render(request,"signup.html",{'site_info_data':site_info_data,'reg_form':reg_form,'product_meta_data':meta_data()})
from extraPackage.mailer import login_detect
def login(request):
    if request.method == "POST":
        usrid = dataValidate(request.POST['usrId'])
        passwd = request.POST['password']
        
        if(validate_email(usrid)):
            usr = auth.authenticate(email=usrid,password=passwd)
        else:
            usr = auth.authenticate(username=usrid,password=passwd)

        if usr is not None:
            auth.login(request,usr)
            data = {'user':request.user}
            login_detect(data)
            return HttpResponse("success")
        else:
            return HttpResponse("invalid")
    else:
        return render(request,"signin.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return HttpResponse("success")
    else:
        return redirect("/")
        
def send_reset_link(mail):
    # Sending Code goes here...
    pass

def lostPassword(request):
    if request.method=='POST':
        mail = dataValidate(request.POST['email'])
        if(validate_email(mail)):
            try:usrObj = User.objects.get(email=mail)
            except User.DoesNotExist: usrObj = True
            if(usrObj==True):
                return HttpResponse("invalid-user")
            else:
                send_reset_link(mail)
                return HttpResponse("success")
        else:
            return HttpResponse("invalid-email")

    else:
        return render(request,"lost-password.html",{'site_info_data':site_info_data,'product_meta_data':meta_data()})

