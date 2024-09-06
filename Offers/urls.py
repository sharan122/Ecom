from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='Offers'
urlpatterns = [
    
    path('',views.option,name='option'),
    path('product_offer',views.product_offer,name='product_offer'),
    path('add_offer/<int:id>',views.add_offer,name='add_offer'),
    path('edit_offer/<int:id>',views.edit_offer,name='edit_offer'),
    path('delete_offer/<int:id>',views.delete_offer,name='delete_offer'),
    path('brand_offer/<int:id>',views.brand_offer,name='brand_offer'),
    path('edit_brand_offer/<int:id>',views.edit_brand_offer,name='edit_brand_offer'),
    path('brand_offer_list/',views.brand_offer_list,name='brand_offer_list'),
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)