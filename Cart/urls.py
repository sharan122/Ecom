from django.urls import path
from . import views

app_name ='Cart'
urlpatterns = [
    path('',views.view_cart,name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update_qty/',views.update_qty, name='update_qty'),
    path('remove_item/<int:id>/',views.remove_item, name='remove_item'),
    path('check_out/',views.check_out, name='check_out'),
    # path('apply_coupon/',views.apply_coupon, name='apply_coupon'),
]                   