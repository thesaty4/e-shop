from django.contrib import admin
from django.db.models import fields
from .models import *

# Register your models here.

class CustUser(admin.ModelAdmin):
    list_display = ('profile','username','email','account_status',)
    list_filter=("username",)
    # list_editable=("account_status",)

admin.site.register(User,CustUser,)

class CustAdd(admin.ModelAdmin):
    list_display = ('profile','user','is_shipping_details',)
    list_filter=("user","is_shipping_details")
    # list_editable=("account_status",)

admin.site.register(BillingInfo,CustAdd,)
