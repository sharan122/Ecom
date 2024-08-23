from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('',views.users,name='users'),
    path('block/<int:id>/', views.block, name='block'),
    path('user_profile/', views.user_profile, name='user_profile'),
]