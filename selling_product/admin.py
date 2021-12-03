from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((ProductBrand,Category,Subcategory,CategoryImage))
# admin.site.register((product_image,checkout,checkout_tracking,product_review,review_vote))
admin.site.register((ProductImage,ProductReview,ReviewVote,ProductSubscriber,ProductTags,ProductUserViews,ProductViews,TotalViews))
class CustProduct(admin.ModelAdmin):
    list_filter=("add_date_time","is_offer")
    list_display=('item',"title","category","color_code","add_date_time",)
    list_display_link=("title","category",)
    list_editable=("color_code",)
    # save_as = True
    # save_on_top = True
    change_list_template = 'products_graph.html'

admin.site.register(Product,CustProduct)

class CustWishlist(admin.ModelAdmin):
    list_display=("product","customer_user","date_time",)
    list_filter=("date_time",)
admin.site.register(Wishlist,CustWishlist)

class CustOffice(admin.ModelAdmin):
    list_display=("office_code","helpline_number","helpline_email",)
    list_filter=("office_code",)
admin.site.register(Office,CustOffice)

class CustCheckout(admin.ModelAdmin):
    list_display=("item","order_id","p","customer_user","delevery_mode","order_status",)
    list_filter=("order_id","order_status",)
    list_editable=("order_status",)
admin.site.register(Checkout,CustCheckout)

class CustOrder(admin.ModelAdmin):
    list_display=("item","tracking_id","office_code","status",)
    list_filter=("office_code","status",)
    list_editable=("status",)
admin.site.register(OrderTracking,CustOrder)

class CustCheckoutOwner(admin.ModelAdmin):
    list_display=("checkout","item_owner")
    list_filter=("item_owner",)
admin.site.register(CheckoutItemOwner,CustCheckoutOwner)

