from django.shortcuts import render, redirect,get_object_or_404
from .models import Product,variant,Category,Review
from Brands.models import Brand
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
import re
from Offers.models import Product_Offers,Brand_Offers
from Order.models import Order_item
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from Decorators.decorators import user_auth



def is_staff(user):
    return user.is_staff


# Create your views here.
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def add_product(request):
    products=Product.objects.order_by('-id')
    # product_qty_sums = variant.objects.values('p_id').annotate(total_qty=Sum('qty')) 
    
    context={'products':products,
            #  'product_qty_sums':product_qty_sums
             }
    
    return render(request,"add_product/add_product.html",context)





@login_required(login_url='Accounts:admin_login')
@never_cache 
@user_passes_test(is_staff,'Accounts:admin_login')
def create_product(request):
    brands = Brand.objects.filter(status=True)
    categories = Category.objects.filter(is_active=True)
    context = {'brands': brands, 'categories': categories}

    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description').strip()
        camera = request.POST.get('camera').strip()
        display_type = request.POST.get('display_type').strip()
        display_size = request.POST.get('display_size').strip()
        processor = request.POST.get('processor').strip()
        battery = request.POST.get('battery').strip()
        os = request.POST.get('os').strip()
        network_type = request.POST.get('network_type').strip()
        brand_id = request.POST.get('brand')
        category_ids = request.POST.getlist('categories[]')


        if not brand_id or not name or not description:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "add_product/new_products.html", context)

      
        if len(name) < 3:
            messages.error(request, "Product name must be at least 3 characters long.")
            return render(request, "add_product/new_products.html", context)

        if len(description) < 10:
            messages.error(request, "Product description must be at least 10 characters long.")
            return render(request, "add_product/new_products.html", context)


        if not camera.replace('+', '').isdigit():
            messages.error(request, "Camera field should only contain numbers and '+' sign.")
            return render(request, "add_product/new_products.html", context)


        try:
            float_display_size = float(display_size)
        except ValueError:
            messages.error(request, "Display size must be a valid number.")
            return render(request, "add_product/new_products.html", context)

  
        if not battery.isdigit():
            messages.error(request, "Battery field should only contain numbers.")
            return render(request, "add_product/new_products.html", context)

        try:
            brand_instance = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            messages.error(request, "Selected brand does not exist.")
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

        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            new_product.categories.set(categories)

        messages.success(request, "Product created successfully.")
        return redirect('Product:add_product')

    return render(request, "add_product/new_products.html", context)






@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    brands = Brand.objects.filter(status=True)
    categories = Category.objects.filter(is_active=True)
    context = {'product': product, 'brands': brands, 'categories': categories}
    
    if request.method == "POST":
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
        category_ids = request.POST.getlist('categories[]')
        
        # Validations
        if not name or not description or not brand_id:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "add_product/edit_product.html", context)

        if len(name) < 3:
            messages.error(request, "Product name must be at least 3 characters long.")
            return render(request, "add_product/edit_product.html", context)

        if len(description) < 10:
            messages.error(request, "Product description must be at least 10 characters long.")
            return render(request, "add_product/edit_product.html", context)

        if not camera.replace('+', '').isdigit():
            messages.error(request, "Camera field should only contain numbers and '+' sign.")
            return render(request, "add_product/edit_product.html", context)

        try:
            float_display_size = float(display_size)
        except ValueError:
            messages.error(request, "Display size must be a valid number.")
            return render(request, "add_product/edit_product.html", context)

        if not battery.isdigit():
            messages.error(request, "Battery field should only contain numbers.")
            return render(request, "add_product/edit_product.html", context)

        try:
            brand_instance = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            messages.error(request, "Selected brand does not exist.")
            return render(request, "add_product/edit_product.html", context)

        # Update Product instance
        product.name = name
        product.description = description
        product.camera = camera
        product.display_type = display_type
        product.display_size = float_display_size  # Update with the converted float
        product.processor = processor
        product.battery = battery
        product.os = os
        product.network_type = network_type
        product.brand = brand_instance
        product.save()

        # Update categories
        product.categories.set(category_ids)

        return redirect('Product:add_product') 

    return render(request, 'add_product/edit_product.html', context)

#-----------------------------VARIENT---------------------

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def view_variant(request,id):
    product = get_object_or_404(Product, pk=id)  
    varients=variant.objects.filter(p_id=id)
    
    product_offer=None
    for varinent_id in varients:
        try:
            product_offer = Product_Offers.objects.get(product_id=varinent_id.id)      

        except:
             product_offer=None
          
    context={
        'products':varients,
        'product': product,
        'p_offer':product_offer
        }
    return render(request,"add_product/varients.html",context)


@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def add_new_varient(request, id):
    products = get_object_or_404(Product, pk=id)
    context = {
        'varients': products,
        'product_id': products
        
        }
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

        if not qty or not qty.isdigit() or int(qty) < 0:
            messages.error(request, 'Please enter a valid quantity.')
            return redirect(request.path_info)

        if not price or not price.replace('.', '', 1).isdigit() or float(price) < 0:
            messages.error(request, 'Please enter a valid price.')
            return redirect(request.path_info)

        # Duplicate check
        if variant.objects.filter(ram=ram, rom=rom, color=color).exists():
            messages.warning(request, 'Variant already exists.')
            return redirect(request.path_info)

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
        if variant.objects.filter(ram=ram,rom=rom,color=color).exists():
            messages.warning(request,'variant is already exist')
            return redirect(request.path_info)
        new_variant_instance.save()

    return render(request, "add_product/add_varient.html", context)

       


@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
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
@user_passes_test(is_staff,'/')
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
        
        if not qty.isdigit() or int(qty) <0:
            messages.error(request, "Quantity must be a positive integer.")
            return render(request, 'add_product/edit_varient.html', context)

        if float(price) <= 0:
            messages.error(request, "Price must be a positive integer.")
            return render(request, 'add_product/edit_varient.html', context)

        # Update the variant
        variants.ram = ram
        variants.rom = rom
        variants.color = color
        variants.qty = qty
        variants.price = price

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
    total=variant.objects.count()
    products=variant.objects.all()
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(status=True)
    
    search = request.POST.get('search')
    if search:
        products = variant.objects.filter(p_id__name__icontains=search)
    
    
    category=request.GET.get('category')
    brand = request.GET.get('brand')
    sort = request.GET.get('select')
    if category:
        products=products.filter(p_id__categories=category)
    if brand:
        products = products.filter(p_id__brand=brand)
        
    if sort == 'a-z':
        products=products.order_by('p_id__name')
    if sort == 'z-a':
        products=products.order_by('-p_id__name')
    if sort == 'new':
        products=products.order_by('-id')
    if sort == 'high':
        products=products.order_by('-price')
    if sort == 'low':
        products=products.order_by('price')
    
    context={
        
        'products':products,
        'categories':categories,
        'total':total,
        'brands':brands
        
        }
    return render(request, 'explore/explore.html', context)


#====================================== single product details =================================

def single_product(request, id):
   
    varient = get_object_or_404(variant, id=id)
    product = varient.p_id
    varient_list = variant.objects.filter(p_id=product)
    reviews = Review.objects.filter(product_id = id)


    try:
        
        brand_offer = Brand_Offers.objects.get(brand_id=varient.p_id.brand.id)
    except Brand_Offers.DoesNotExist:
        brand_offer = None
        
    try:
        
        offer = Product_Offers.objects.get(product_id=id)
        pr_offer = varient.price - (offer.offer_price / 100) * varient.price
    except Product_Offers.DoesNotExist:
        offer = None
        pr_offer = None

    if offer and brand_offer:
       
        b_offer = varient.price - (brand_offer.offer_price / 100) * varient.price
        if offer.offer_price >= brand_offer.offer_price:
            p_offer = pr_offer
            offer_per = offer.offer_price
        else:
            p_offer = b_offer
            offer_per = brand_offer.offer_price
    elif offer:
       
        p_offer = pr_offer
        offer_per = offer.offer_price
    elif brand_offer:
        
        p_offer = varient.price - (brand_offer.offer_price / 100) * varient.price
        offer_per = brand_offer.offer_price
    else:
        
        p_offer = varient.price
        offer_per = 0

    context = {
        'varients': varient,
        'varient_list': varient_list,
        'offer': round(p_offer),
        'percentage': offer_per,
        'reviews':reviews
    }
    return render(request, "single_product/single_product.html", context)
#-------------------------- filters ---------------------------------------

    

#-------------------------------Category-------------------------------------
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        
        # Check if the name is provided
        if not name:
            messages.error(request, 'Category name is required.')
            return render(request, 'category/create_category.html')
        
        # Check if the name contains only white spaces
        if not name.strip():
            messages.error(request, 'Category name cannot contain only white spaces.')
            return render(request, 'category/create_category.html')
        
        # Check if the name contains only alphabets
        if not re.match("^[A-Za-z\s]+$", name):
            messages.error(request, 'Category name can only contain alphabets.')
            return render(request, 'category/create_category.html')
        
        # Check if the name is too short
        if len(name.strip()) < 3:
            messages.error(request, 'Category name must be at least 3 characters long.')
            return render(request, 'category/create_category.html')
        
        # Check if the category already exists
        if Category.objects.filter(name__iexact=name.strip()).exists():
            messages.error(request, 'Category already exists.')
            return render(request, 'category/create_category.html')
        
        # If all validations pass, create the category
        Category.objects.create(name=name.strip())
        messages.success(request, 'Category created successfully!')
        return redirect('Product:category_list')
    
    return render(request, 'category/create_category.html')

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_category(request,id):
    cat_id=get_object_or_404(Category,id=id)
    context={'category':cat_id}
    if request.method=='POST':
        name=request.POST.get('category_name')
        if not name:
            messages.error(request, 'Category name is required.')
            return render(request, 'category/edit_category.html',context)
        
        # Check if the name contains only white spaces
        if not name.strip():
            messages.error(request, 'Category name cannot contain only white spaces.')
            return render(request, 'category/edit_category.html',context)
        
        # Check if the name contains only alphabets
        if not re.match("^[A-Za-z\s]+$", name):
            messages.error(request, 'Category name can only contain alphabets.')
            return render(request, 'category/edit_category.html',context)
        
        # Check if the name is too short
        if len(name.strip()) < 3:
            messages.error(request, 'Category name must be at least 3 characters long.')
            return render(request, 'category/edit_category.html',context)
        
        # Check if the category already exists
        if Category.objects.filter(name__iexact=name.strip()).exists():
            messages.error(request, 'Category already exists.')
            return render(request, 'category/edit_category.html',context)
        
        cat_id.name=name
        cat_id.save() 
        messages.success(request, 'Category created successfully!')
        return redirect('Product:category_list')
    return render(request, 'category/edit_category.html',context)
    

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def category_list(request):
    category=Category.objects.all()
    context={'categorys':category}
    return render(request,'category/category_list.html',context)

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def block_category(request,id):
    cat_id=get_object_or_404(Category,id=id)
    cat_id.is_active = not cat_id.is_active
    cat_id.save()
    return redirect('Product:category_list')

#======================= review ===========================================
@user_auth
@require_POST
def review(request, id):
    review = request.POST.get('review')
    order_item_id = request.POST.get('order_item_id')
    order_item = get_object_or_404(Order_item, id=order_item_id)
    product = get_object_or_404(variant, id=id)
    
    Review.objects.create(
        product_id=product,
        user_id=request.user,
        review=review            
    )
    
    return JsonResponse({'success': True})