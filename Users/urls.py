from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('',views.users,name='users'),
    path('block/<int:id>/', views.block, name='block'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('new_address/', views.new_address, name='new_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('all_address/', views.all_address, name='all_address'),
    path('edit_details/', views.edit_details, name='edit_details'),
     path('add-new-address/', views.add_new_address, name='add_new_address'),
]