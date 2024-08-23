from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Product.models import Product,variant 
from Decorators.decorators import user_auth
from Product.views import is_staff

# Create your views here.

def user_home(request):
    if not request.user.is_active:
        return redirect('Accounts:user_login')
    products=variant.objects.all()
    context={'products':products}
    return render(request,"home_page/index.html",context)


@user_auth
@user_passes_test(is_staff,'Accounts:admin_login')
@login_required(login_url='Accounts:admin_login')
@never_cache
def admin_home(request):
    return render(request,"admin_home/index.html")
     
