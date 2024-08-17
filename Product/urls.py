from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Product'
urlpatterns = [
    path('',views.add_product,name='add_product'),
    path('create_product/',views.create_product,name='create_product'),
    
    path('variants/<int:id>', views.view_variant,name='view_variant'),
    
    path('add_new_variants/<int:id>', views.add_new_varient,name='add_new_varient'),
    path('variants_details/<int:id>', views.varient_details,name='varient_details'),
    path('edit_product/<int:id>', views.edit_product,name='edit_product'),
    path('edit_variant/<int:id>', views.edit_variant,name='edit_variant'),
    path('explore/', views.explore,name='explore'),
    path('signle_product/<int:id>', views.signle_product,name='signle_product'),
    path('block_varient/<int:id>/', views.block_varient, name='block_varient'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)