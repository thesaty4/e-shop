# // @Author SATYA NARAYAN MISHRA
from django.urls import path
from . import views
urlpatterns = [
    path("register/",views.register,name='register'),
    path("login/",views.login,name='login'),
    path("lostPassword/",views.lostPassword,name='lost-password'),
    path("logout/",views.logout,name='logout'),
    ]