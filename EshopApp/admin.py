from django.contrib import admin
from .models import AboutSite, BackgroundBanner, ContactUs, ContactUsInfo, Faq, NewsLetter, ShopByDealsImage, SiteOffer, Slider, Subscriber,SiteInfo, TitleOfFaq

# Register your models here.
admin.site.register((TitleOfFaq,Faq,NewsLetter,ShopByDealsImage))
admin.site.register((Subscriber,ContactUs,ContactUsInfo,SiteOffer,AboutSite,Slider,BackgroundBanner))

class CustSiteInfo(admin.ModelAdmin):
    list_display=('site_logo','shop_name','email',)
    # list_clickable=('site_logo','shop_name','email',)
admin.site.register(SiteInfo,CustSiteInfo)
