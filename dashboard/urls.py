from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashMyProfile/',views.dashMyProfile,name='dash-my-profile'),
    path('dashAddressBook/',views.dashAddressBook,name='dash-address-book'),
    path('dashTrackOrder/',views.dashTrackOrder,name='dash-track-order'),
    path('dashMyOrder/',views.dashMyOrder,name='dash-my-order'),
    path('dashPaymentOption/',views.dashPaymentOption,name='dash-payment-option'),
    path('dashCancellation/',views.dashCancellation,name='dash-cancellation'),
    path('returned-order/',views.dashReturning,name='dash-returning'),
    path('dashEditProfile/',views.dashEditProfile,name='dash-edit-profile'),
    path('dashManageOrder/<str:order_id>',views.dashManageOrder,name='dash-manage-order'),
    path('dashAddMakeDefault/',views.dashAddMakeDefault,name='dash-address-make-default'),
    path('dash-change-password/',views.dashChangePass,name='Password Changing'),
    path('dashAddressAdd/',views.dashAddressAdd,name='dash-address-add'),
    path('dashAddressEdit/<int:addressId>/',views.dashAddressEdit,name='dash-address-edit'),
    path("update-user-profile/",views.profileUpdate,name='User Record updating'),
    path("update-profile-pic/",views.updateProfilePic,name="Update Profile Pic"),
    path("verify-password/",views.verifyPassword,name="password verifying"),
    path("change-password/",views.changePassword,name="Change Password"),
    path("delete-address/",views.deleteAddress,name="Delete Address"),
    path("my-order-sort/",views.myOrderSort,name="order sorting"),

]