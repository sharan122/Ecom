from django.shortcuts import render, redirect,get_object_or_404
from .models import variant
from Brands.models import Brand
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Offers.models import Product_Offers,Brand_Offers
from django.contrib import messages
# Create your views here.


#=================== add new product offer ====================
def add_offer(request,id):
    if request.method == 'POST':
        product = get_object_or_404(variant,id=id)
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')
        if Product_Offers.objects.filter(product_id=product).exists():
            messages.error(request,'Offer Already Exists!!!')
            return redirect(request.path_info)

        Product_Offers.objects.create(
           product_id =  product,
           offer_price = amount,
           offer_name = name,
           offer_details = description
        )
        return redirect('Product:view_variant',id=product.p_id.id)
    return render(request,'offers/add_offer.html')
#=========================== select offer option ===========================
def option(request):
    return render(request,'offers/options.html') 
#======================= product offers ====================================
def product_offer(request):
    offers = Product_Offers.objects.all()
    context = {
        
        'offers':offers
    }
    return render(request,'offers/product_offer.html',context)

#================================== edit offer ========================

def edit_offer(request,id):
    offer = get_object_or_404(Product_Offers,id=id)
    context = {
        'offer':offer
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')

        offer.offer_name = name
        offer.offer_details = description
        offer.offer_price = amount
        offer.save()
        return redirect('Offers:product_offer')
    return render(request,'offers/add_offer.html',context)
#============================== delete brand offer ===========================

def delete_offer(request,id):
    offer = get_object_or_404(Product_Offers,id=id)
    offer.delete()
    return redirect('Offers:product_offer')

#=================================== brand offer ==============================
def brand_offer(request,id):
    if request.method == 'POST':
        brand = get_object_or_404(Brand,id=id)
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')
        if Brand_Offers.objects.filter(brand_id=brand).exists():
            messages.error(request,'Offer Already Exists!!!')
            return redirect(request.path_info)
        Brand_Offers.objects.create(
           brand_id =  brand,
           offer_price = amount,
           offer_name = name,
           offer_details = description
        )
        return redirect('Brands:brands_list')
    return render(request,'offers/add_brand_offer.html')

#================================ edit brand offer ================================

def edit_brand_offer(request,id):
    offer = get_object_or_404(Brand_Offers,id=id)
    context = {
        'offer':offer
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        description = request.POST.get('description')

        offer.offer_name = name
        offer.offer_details = description
        offer.offer_price = amount
        offer.save()
        return redirect('Offers:product_offer')
    return render(request,'offers/add_brand_offer.html',context)

#================================ all brand offers =================================

def brand_offer_list(request):
    offers = Brand_Offers.objects.all()
    context = {
        'offers':offers
    }
    return render(request,'offers/brand_offers.html',context)