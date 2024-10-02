from django.shortcuts import render, redirect,get_object_or_404
from .models import variant
from Brands.models import Brand
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Offers.models import Product_Offers,Brand_Offers
from django.contrib import messages
# Create your views here.

def is_staff(user):
    return user.is_staff

#=================== add new product offer ====================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def add_offer(request, id):
    if request.method == 'POST':
        product = get_object_or_404(variant, id=id)
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')

      
        errors = False

  
        try:
            amount = float(amount)
            if amount <= 0 or amount > 100:
                messages.error(request, "Offer price must be a positive number.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Offer price must be a valid number.")
            errors = True

        if not name:
            messages.error(request, "Offer name is required.")
            errors = True
        elif len(name) < 3:
            messages.error(request, "Offer name must be at least 3 characters long.")
            errors = True

    
        if not description:
            messages.error(request, "Offer description is required.")
            errors = True
        elif len(description) < 10:
            messages.error(request, "Offer description must be at least 10 characters long.")
            errors = True

        if Product_Offers.objects.filter(product_id=product).exists():
            messages.error(request, "Offer already exists for this product!")
            errors = True

       
        if not errors:
            Product_Offers.objects.create(
                product_id=product,
                offer_price= int(amount),
                offer_name=name,
                offer_details=description
            )
            messages.success(request, "Offer created successfully!")
            return redirect('Product:view_variant', id=product.p_id.id)

    return render(request, 'offers/add_offer.html')

#=========================== select offer option ===========================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def option(request):
    return render(request,'offers/options.html') 
#======================= product offers ====================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def product_offer(request):
    offers = Product_Offers.objects.all()
    context = {
        
        'offers':offers
    }
    return render(request,'offers/product_offer.html',context)

#================================== edit product  offer ========================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_offer(request, id):
    offer = get_object_or_404(Product_Offers, id=id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validation
        errors = False

        # Validate amount (should be a positive number and <= 100 since it's a percentage)
        try:
            amount = float(amount)
            if amount <= 0 or amount > 100:
                messages.error(request, "Offer percentage must be between 1 and 100.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Offer percentage must be a valid number.")
            errors = True

        # Validate name
        if not name:
            messages.error(request, "Offer name is required.")
            errors = True
        elif len(name) < 3:
            messages.error(request, "Offer name must be at least 3 characters long.")
            errors = True

        # Validate description
        if not description:
            messages.error(request, "Offer description is required.")
            errors = True
        elif len(description) < 10:
            messages.error(request, "Offer description must be at least 10 characters long.")
            errors = True

        # If no errors, update the offer
        if not errors:
            offer.offer_name = name
            offer.offer_details = description
            offer.offer_price = round(amount) 
            offer.save()

            messages.success(request, "Offer updated successfully!")
            return redirect('Offers:product_offer')

    context = {
        'offer': offer
    }
    return render(request, 'offers/add_offer.html', context)

#============================== delete brand offer ===========================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def delete_offer(request,id):
    offer = get_object_or_404(Product_Offers,id=id)
    offer.delete()
    return redirect('Offers:product_offer')

#=================================== brand offer ==============================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def brand_offer(request, id):
    if request.method == 'POST':
        brand = get_object_or_404(Brand, id=id)
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')

        
        errors = False

        try:
            amount = float(amount)
            if amount <= 0 or amount > 100:
                messages.error(request, "Offer percentage must be between 1 and 100.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Offer percentage must be a valid number.")
            errors = True

        if not name:
            messages.error(request, "Offer name is required.")
            errors = True
        elif len(name) < 3:
            messages.error(request, "Offer name must be at least 3 characters long.")
            errors = True


        if not description:
            messages.error(request, "Offer description is required.")
            errors = True
        elif len(description) < 10:
            messages.error(request, "Offer description must be at least 10 characters long.")
            errors = True


        if Brand_Offers.objects.filter(brand_id=brand).exists():
            messages.error(request, "Offer already exists for this brand!")
            errors = True

        if not errors:
            Brand_Offers.objects.create(
                brand_id=brand,
                offer_price=amount,
                offer_name=name,
                offer_details=description
            )
            messages.success(request, "Brand offer created successfully!")
            return redirect('Brands:brands_list')

    return render(request, 'offers/add_brand_offer.html')


#================================ edit brand offer ================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_brand_offer(request, id):
    offer = get_object_or_404(Brand_Offers, id=id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')


        errors = False


        try:
            amount = float(amount)
            if amount <= 0 or amount > 100:
                messages.error(request, "Offer percentage must be between 1 and 100.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Offer percentage must be a valid number.")
            errors = True

        if not name:
            messages.error(request, "Offer name is required.")
            errors = True
        elif len(name) < 3:
            messages.error(request, "Offer name must be at least 3 characters long.")
            errors = True

        if not description:
            messages.error(request, "Offer description is required.")
            errors = True
        elif len(description) < 10:
            messages.error(request, "Offer description must be at least 10 characters long.")
            errors = True


        if not errors:
            offer.offer_name = name
            offer.offer_details = description
            offer.offer_price = amount
            offer.save()

            messages.success(request, "Brand offer updated successfully!")
            return redirect('Offers:brand_offer_list')

    context = {
        'offer': offer
    }
    return render(request, 'offers/add_brand_offer.html', context)

#================================ all brand offers =================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def brand_offer_list(request):
    offers = Brand_Offers.objects.all()
    context = {
        'offers':offers
    }
    return render(request,'offers/brand_offers.html',context)