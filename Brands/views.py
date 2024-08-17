from django.shortcuts import render,get_object_or_404,redirect
from .models import Brand
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required(login_url='Accounts:admin_login')
@never_cache
def brands_list(request):
    brands=Brand.objects.all()
    context={'brands':brands}
    return render(request,'brand/brands_list.html',context)

@login_required(login_url='Accounts:admin_login')
@never_cache
def create_brand(request):
    if request.method=="POST":
        brand_name=request.POST.get('brand_name')
        brand_instance=Brand(brand_name=brand_name)
        brand_instance.save()
    return render(request,'brand/create_brands.html')

def block_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    brand.status = not brand.status
    brand.save()
    return redirect('Brands:brands_list')
