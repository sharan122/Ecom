from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='Order'
urlpatterns = [
    path('',views.place_order,name='place_order'),
    path('order_list/',views.order_list,name='order_list'),
    path('all_order/',views.user_order,name='user_order'),
    path('order_items/<int:id>',views.order_items,name='order_items'),
    path('user_order_details/<int:id>',views.user_order_details,name='user_order_details'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancel_order'),
    path('order_status/<int:id>',views.order_status,name='order_status'),
    path('request_return/<int:id>',views.request_return,name='request_return'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('verify_payment/',views.verify_payment,name='verify_payment'),
    path('success/',views.success,name='success'),
    path('retry_payment/<int:order_id>/', views.retry_payment, name='retry_payment'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    path('remove_coupon/',views.remove_coupon,name='remove_coupon'),
    path('download-invoice/<int:order_item_id>/', views.generate_invoice, name='download_invoice')
  
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)