from django.urls import path
from . import views


app_name ='Coupons'
urlpatterns = [
    path('add_coupon/',views.add_coupon,name='add_coupon'),
    path('',views.all_coupond,name='all_coupond'),
    path('edit_coupon/<int:id>',views.edit_coupon,name='edit_coupon'),
    path('remove_coupon/<int:id>',views.remove_coupon,name='remove_coupon'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
  
    
    
]