from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ='Wishlist'
urlpatterns = [
    
    path('',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:id>',views.add_wishlist,name='add_wishlist'),
    path('remove_wishlist/<int:id>',views.remove_wishlist,name='remove_wishlist'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)