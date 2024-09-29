from django.urls import path
from . import views
app_name ='Wallet'
urlpatterns = [
    path('',views.transactions,name='transactions')

  
    
]