from django.shortcuts import render,get_object_or_404,redirect
from .models import Brand
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
import re
from Product.views import is_staff
from Offers.models import Brand_Offers


@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def brands_list(request):
    brands = Brand.objects.all()
    
    # Add offer information directly to the brand objects
    for brand in brands:
        brand_offer = Brand_Offers.objects.filter(brand_id=brand.id, status=True).first()
        brand.offer = brand_offer  # Attach the offer to the brand object

    context = {'brands': brands}
    return render(request, 'brand/brands_list.html', context)


@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def create_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get('brand_name')

        # Check if brand name is provided
        if not brand_name:
            messages.error(request, 'Brand name is required.')
            return render(request, 'brand/create_brands.html')

        # Check if the brand name contains only white spaces
        if not brand_name.strip():
            messages.error(request, 'Brand name cannot contain only white spaces.')
            return render(request, 'brand/create_brands.html')

        # Check if the brand name is too short
        if len(brand_name.strip()) < 1:
            messages.error(request, 'Brand name must be at least 1 characters long.')
            return render(request, 'brand/create_brands.html')

        # Check if the brand name already exists
        if Brand.objects.filter(brand_name__iexact=(brand_name).strip()).exists():
            messages.error(request, 'Brand already exists.')
            return render(request, 'brand/create_brands.html')

        # If all checks pass, save the new brand
        brand_instance = Brand(brand_name=brand_name.strip())
        brand_instance.save()
        messages.success(request, 'Brand created successfully!')
        return redirect('Product:brand_list')  # Redirect to a relevant page after successful creation

    return render(request, 'brand/create_brands.html')

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_brand(request,id):
    brand_id=get_object_or_404(Brand,id=id)
    context={'brand_id':brand_id}
    if request.method=="POST":
        brand_name=request.POST.get('brand_name')
        if not brand_name:
            messages.error(request, 'Brand name is required.')
            return render(request, 'brand/edit_brands.html',context)


        # Check if the brand name contains only white spaces
        if not brand_name.strip():
            messages.error(request, 'Brand name cannot contain only white spaces.')
            return render(request, 'brand/edit_brands.html',context)


        # Check if the brand name is too short
        if len(brand_name.strip()) < 2:
            messages.error(request, 'Brand name must be at least 1 characters long.')
            return render(request, 'brand/edit_brands.html',context)

        # Check if the brand name already exists
        if Brand.objects.filter(brand_name__iexact=brand_name.strip()).exists():
            messages.error(request, 'Brand already exists.')
            return render(request, 'brand/edit_brands.html',context)
        
        if re.search(r'[@!#$%^&*()_+={}\[\]:;"\'<>,.?\\|`~\-]{2,}', brand_name):
            messages.error(request, 'Brand name cannot contain continuous special characters.')
            return render(request, 'brand/edit_brands.html', context)
         
        if re.search(r'\d{2,}', brand_name):
            messages.error(request, 'Brand name cannot contain continuous numbers.')
            return render(request, 'brand/edit_brands.html', context)
        
        brand_id.brand_name=brand_name
        brand_id.save()
        return redirect('Brands:brands_list')
    return render(request,'brand/edit_brands.html',context)
 

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def block_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    brand.status = not brand.status
    brand.save()
    return redirect('Brands:brands_list')
