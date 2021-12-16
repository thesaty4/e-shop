from .models import ClickCounter, ClickProduct, ClickCategory, ClickSubcategory, RecentQuery
from django.contrib import admin
# Register your models here.
admin.site.register((RecentQuery,ClickCounter,ClickProduct,ClickCategory,ClickSubcategory))