"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import debug_toolbar
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_title = "E-Shop"
admin.site.site_header = "Welcome To E-Shop"
# admin.site.index_template='admin-cutomizer/base_site.html'
# admin.autodiscover()
urlpatterns = [
    path('',include("EshopApp.urls")),
    path('admin/', admin.site.urls),
    path('accounts/',include("accounts.urls")),
    path('dashboard/',include("dashboard.urls")),
    path('blogs/',include("blogs.urls")),
    path('productDetails/',include("EshopApp.urls")),
    path('shop/',include("EshopApp.urls")),
    path('wishlist/',include("EshopApp.urls")),
    path('checkout/',include("EshopApp.urls")), 
    path('faq/',include("EshopApp.urls")),
    path('contact/',include("EshopApp.urls")),
    path('about/',include("EshopApp.urls")),
    path('pnf404/',include("EshopApp.urls")),
    path('about/',include("EshopApp.urls")),
    path('cart/',include("EshopApp.urls")),
    path('emptyCart/',include("EshopApp.urls")),
    path('emptyWishlist/',include("EshopApp.urls")),
    path('emptySearch/',include("EshopApp.urls")),
    path('selling_product/',include("selling_product.urls")),
    path(r'^tinymce/', include('tinymce.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


