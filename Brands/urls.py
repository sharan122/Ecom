from django.urls import path
from . import views

app_name ='Brands'
urlpatterns = [
    path('',views.brands_list,name='brands_list'),
    path('create_brand/',views.create_brand,name='create_brand'),
    path('block_brand/<int:id>/', views.block_brand, name='block_brand'),
    path('edit_brand/<int:id>/', views.edit_brand, name='edit_brand'),
]