from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from Product.models import Product,variant 
# Create your views here.
def user_home(request):
    products=variant.objects.filter(status=True)
    context={'products':products}
    return render(request,"home_page/index.html",context)

@login_required(login_url='Accounts:admin_login')
@never_cache
def admin_home(request):
    return render(request,"admin_home/index.html")
     
