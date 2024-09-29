from django.urls import path
from . import views
from django.shortcuts import render

app_name= 'Accounts'

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('signup/',views.user_signup,name='user_signup'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('logout_admin/',views.logout_admin,name='logout_admin'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    path('resend_otp/',views.resend_otp, name='resend_otp'),
    path('change_password/',views.change_password, name='change_password'),
    path('set_password/',views.set_password, name='set_password'),
    
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_done/', lambda request: render(request, 'forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', lambda request: render(request, 'forgot_password/password_reset_complete.html'), name='password_reset_complete'),
]