from django.urls import path
from . import views

app_name= 'Accounts'

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('signup/',views.user_signup,name='user_signup'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('logout_admin/',views.logout_admin,name='logout_admin'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    path('resend_otp/',views.resend_otp, name='resend_otp'),
]