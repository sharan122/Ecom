from django.urls import path
from . import views

app_name = 'Home'
urlpatterns = [
    path('',views.user_home,name='user_home'),
    path('admin-home/',views.admin_home,name='admin_home')    
]