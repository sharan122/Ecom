from django.shortcuts import render, redirect,get_object_or_404
from .models import Product,variant 
from Brands.models import Brand
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.
@login_required(login_url='Accounts:admin_login')
@never_cache
def add_product(request):
    products=Product.objects.all()
    # product_qty_sums = variant.objects.values('p_id').annotate(total_qty=Sum('qty'))
    
    context={'products':products,
            #  'product_qty_sums':product_qty_sums
             }
    
    return render(request,"add_product/add_product.html",context)



@login_required(login_url='Accounts:admin_login')
@never_cache
def create_product(request):
    brands = Brand.objects.filter(status=True)
    context = {'brands': brands}

    if request.method == 'POST':
       
        name = request.POST.get('name')
        description = request.POST.get('description')
        camera = request.POST.get('camera')
        display_type = request.POST.get('display_type')
        display_size = request.POST.get('display_size')
        processor = request.POST.get('processor')
        battery = request.POST.get('battery')
        os = request.POST.get('os')
        network_type = request.POST.get('network_type')
        brand_id = request.POST.get('brand')

        
        if not brand_id or not name or not description:
            
            context['error'] = "Please fill in all required fields."
            return render(request, "add_product/new_products.html", context)

        try:
            brand_instance = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            context['error'] = "Selected brand does not exist."
            return render(request, "add_product/new_products.html", context)

      
        new_product = Product(
            name=name,
            description=description,
            camera=camera,
            display_type=display_type,
            display_size=display_size,
            processor=processor,
            battery=battery,
            os=os,
            network_type=network_type,
            brand=brand_instance,
        )
        new_product.save()
        return redirect('Product:add_product')
       

    return render(request, "add_product/new_products.html", context)

@login_required(login_url='Accounts:admin_login')
@never_cache
def edit_product(request,id):
    product = get_object_or_404(Product, id=id)
    brands = Brand.objects.filter(status=True)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.camera = request.POST.get('camera')
        product.display_type = request.POST.get('display_type')
        product.display_size = request.POST.get('display_size')
        product.processor = request.POST.get('processor')
        product.battery = request.POST.get('battery')
        product.os = request.POST.get('os')
        product.network_type = request.POST.get('network_type')
        product.brand_id = request.POST.get('brand')
        product.save()
        return redirect('Product:add_product') 

    return render(request, 'add_product/edit_product.html', {'product': product, 'brands': brands})

#-----------------------------VARIENT---------------------

@login_required(login_url='Accounts:admin_login')
@never_cache
def view_variant(request,id):
    product = get_object_or_404(Product, pk=id)  
    varients=variant.objects.filter(p_id=id)
    context={'products':varients,'product': product}                 
    return render(request,"add_product/varients.html",context)


@login_required(login_url='Accounts:admin_login')
@never_cache
def add_new_varient(request, id):
    products = get_object_or_404(Product, pk=id)
    context = {'varients': products, 'product_id': products}
    if request.method == 'POST':
        ram = request.POST.get('ram')
        rom = request.POST.get('rom')
        color = request.POST.get('color')
        qty = request.POST.get('qty')
        price = request.POST.get('price')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        new_variant_instance = variant(
            ram=ram,
            rom=rom,
            color=color,
            qty=qty,
            price=price,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            p_id=products
        )
        new_variant_instance.save()

    return render(request, "add_product/add_varient.html", context)
       


@login_required(login_url='Accounts:admin_login')
@never_cache
def varient_details(request,id):
    varient=variant.objects.filter(id=id)
    context={'varients':varient}
    return render(request,"add_product/varient_details.html",context)

def block_varient(request, id):
    product = get_object_or_404(variant, id=id)
    product.status = not product.status
    product.save()
    return redirect('Product:view_variant',id=product.p_id.id)



@login_required(login_url='Accounts:admin_login')
@never_cache
def edit_variant(request, id):
    variants = get_object_or_404(variant, id=id)
    products = Product.objects.all()
    context= {'variant': variants, 'products': products}
    if request.method == "POST":
        ram = request.POST.get('ram')
        rom = request.POST.get('rom')
        color = request.POST.get('color')
        qty = request.POST.get('qty')
        price = request.POST.get('price')
        
        if not qty.isdigit() or int(qty) <= 0:
            messages.error(request, "Quantity must be a positive integer.")
            return render(request, 'add_product/edit_varient.html', context)

        if not price.isdigit() or int(price) <= 0:
            messages.error(request, "Price must be a positive integer.")
            return render(request, 'add_product/edit_varient.html', context)

        # Update the variant
        variant.ram = ram
        variant.rom = rom
        variant.color = color
        variant.qty = int(qty)
        variant.price = int(price)

        if'image1'in request.FILES:
            variants.image1 = request.FILES['image1']
        if'image2'in request.FILES:
            variants.image2 = request.FILES['image2']
        if'image3'in request.FILES:
            variants.image3 = request.FILES['image3']
        if'image4'in request.FILES:
            variants.image4 = request.FILES['image4']

        variants.save()
        return redirect('Product:view_variant',id=variants.p_id.id) 
    return render(request, 'add_product/edit_varient.html', context)



#-----------------------------Explore page-----------------------------------

def explore(request):
    products=variant.objects.filter(qty__gt=0, status=True)
    context={'products':products}
    return render(request, 'explore/explore.html', context)

def signle_product(request,id):
    varient=variant.objects.filter(id=id)
    context={'varients':varient}
    return render(request,"single_product/single_product.html",context)