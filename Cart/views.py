from django.shortcuts import render,get_object_or_404,redirect
from Cart.models import Cart,Cart_item
from Product.models import variant
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Count
from django.contrib import messages
from Users.models import Address
from Decorators.decorators import user_auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# Create your views here.
@user_auth
@login_required(login_url='Accounts:user_login')
def view_cart(request):
    
    if not request.user.is_authenticated:
        return redirect('Accounts:user:login')
    
    user, _ =Cart.objects.get_or_create(user_id=request.user)
    cart_items = Cart_item.objects.filter(cart=user)
    qty = Cart_item.objects.values('cart_id').annotate(total=Count('id'))
    context={'products':cart_items,'qty':qty}
    
    return render(request,'cart/cart.html',context)


#--------------------- ADD TO CART -----------------------------------

@user_auth
@login_required(login_url='Accounts:user_login')
@require_POST
def add_to_cart(request):
    v_id = request.POST.get('variant_id')
    
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'User not authenticated',
            'redirect': reverse('Accounts:user_login')  
        }, status=401)
    
    product_id = get_object_or_404(variant, id=v_id)
    
    cart_user, _ = Cart.objects.get_or_create(user_id=request.user)
    
    if Cart_item.objects.filter(product=product_id, cart=cart_user).exists():
        return JsonResponse({'success': False, 'message': 'Selected item already in cart'})
    
    Cart_item.objects.create(product=product_id, cart=cart_user)
    return JsonResponse({'success': True, 'message': 'Item added to cart'})


#-------------------------- INCREASE QTY -------------------------------
@user_auth
@login_required(login_url='Accounts:user_login')
def update_qty(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        id = request.POST.get('productid')
        
        if action not in ['increase', 'decrease']:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

        variant_id = get_object_or_404(variant, id=id)
        cart = get_object_or_404(Cart, user_id=request.user.id)
        cart_item = get_object_or_404(Cart_item, product=variant_id, cart=cart)

        if action == 'increase':
            new_quantity = cart_item.qty + 1
            if new_quantity > variant_id.qty or new_quantity > 10:
                return JsonResponse({'status': 'error', 'message': 'Quantity exceeded'}, status=400)
            cart_item.qty = new_quantity

        elif action == 'decrease':
            new_quantity = cart_item.qty - 1
            if new_quantity < 1:
                return JsonResponse({'status': 'error', 'message': 'Quantity cannot be less than 1'}, status=400)
            cart_item.qty = new_quantity

        cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Quantity updated', 'new_quantity': cart_item.qty})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
     
     
#================================= remove item ============================================
@user_auth
@login_required(login_url='Accounts:user_login')
def remove_item(request,id):
    item= get_object_or_404(Cart_item,id=id)
    item.delete()
    return redirect('Cart:view_cart')


#==================================== check out ============================================
@user_auth
@never_cache
@login_required(login_url='Accounts:user_login')
def check_out(request):

    user_id=request.user
    address=Address.objects.filter(user=user_id)
    cart_id = get_object_or_404(Cart,user_id=user_id)
    cart_items = Cart_item.objects.filter(cart=cart_id)
    if not cart_items.exists():
                messages.warning(request,'Cart is empty')
                return redirect('Cart:view_cart')
    for product in cart_items:
        for product in cart_items:
            
            if product.product.p_id.brand.status == False:
                
                messages.warning(request,f'Sorry {product.product.p_id.brand.brand_name} products are not available')
                product.delete()
                return redirect('Cart:view_cart')
                
            if product.product.status == False :
                messages.warning(request,f'{product.product.p_id.name} not available')
                product.delete()
                return redirect('Cart:view_cart')
            if product.product.qty == 0  :
                product.delete()
                messages.warning(request,'Out of stock!!')
                return redirect('Cart:view_cart')
            if product.qty > product.product.qty:
                product.delete()
                messages.warning(request,'Quantity not availale')
                return redirect('Cart:view_cart')
    items_with_totals = [
        (item, item.product.price * item.qty)
        for item in cart_items
    ]
      
    sub_total = sum(item.product.price * item.qty for item in cart_items)
    
    context = {
        'addresses': address,
        'items_with_totals' :  items_with_totals,
        'subtotal' : sub_total
    }
    return render(request,'check_out/check_out.html',context)