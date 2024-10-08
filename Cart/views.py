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
from Offers.models import Brand_Offers,Product_Offers

from Coupons.models import Coupons,Coupon_users


# Create your views here.
@user_auth
@login_required(login_url='Accounts:user_login')
def view_cart(request):
    user, _ = Cart.objects.get_or_create(user_id=request.user)
    cart_items = Cart_item.objects.filter(cart=user)
    
   
    # for item in cart_items:
    #     offers = Product_Offers.objects.filter(product_id=item.product.pk).first()
    #     if offers:
    #         item.offer_price = item.product.price - (offers.offer_price / 100) * item.product.price
    #     else:
    #         item.offer_price = item.product.price  
    qty = Cart_item.objects.values('cart_id').annotate(total=Count('id'))
    
    context = {'products': cart_items, 'qty': qty}
    
    return render(request, 'cart/cart.html', context)


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
    
    variant_id = get_object_or_404(variant, id=v_id)
    
    cart_user, _ = Cart.objects.get_or_create(user_id=request.user)
    
    offers = Product_Offers.objects.filter(product_id=variant_id.pk)
    brand_offers = Brand_Offers.objects.filter(brand_id=variant_id.p_id.brand.pk)

    if Cart_item.objects.filter(product=variant_id, cart=cart_user).exists():
        return JsonResponse({'success': False, 'message': 'Selected item already in cart'})

    # Apply product offer if available
    if offers.exists():
        product_offer_price = variant_id.price - (offers.first().offer_price / 100) * variant_id.price
        
    # Apply brand offer if available
    if brand_offers.exists():
        brand_offer_price = variant_id.price - (brand_offers.first().offer_price / 100) * variant_id.price
        
    # Choose the better offer
    if offers.exists() and brand_offers.exists():
        offer_price = min(product_offer_price, brand_offer_price)
    elif offers.exists():
        offer_price = product_offer_price
    elif brand_offers.exists():
        offer_price = brand_offer_price
    else:
        offer_price = variant_id.price

    Cart_item.objects.create(product=variant_id, cart=cart_user, price=offer_price)

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
    coupon_amount = request.session.get('final_price',0)
    if coupon_amount > 0:
        request.session.pop('coupon_code', None)
        request.session.pop('final_price', None)
        request.session.pop('coupon_amount', None)
    return redirect('Cart:view_cart')


#==================================== check out ============================================
@user_auth
@never_cache
@login_required(login_url='Accounts:user_login')
def check_out(request):
    user_id = request.user
    address = Address.objects.filter(user=user_id)
    cart_id = get_object_or_404(Cart, user_id=user_id)
    cart_items = Cart_item.objects.filter(cart=cart_id)
    coupons = Coupons.objects.filter(status=True)

    final_price = request.session.get('final_price', None)
    coupon_amount = request.session.get('coupon_amount', None)
    coupon_code = request.session.get('coupon_code', None)

    # Check if cart is empty
    if not cart_items.exists():
        messages.warning(request, 'Cart is empty')
        return redirect('Cart:view_cart')

    # Iterate over cart items and check availability
    for product in cart_items:
        if not product.product.p_id.brand.status:
            messages.warning(request, f'Sorry, {product.product.p_id.brand.brand_name} products are not available')
            product.delete()
            return redirect('Cart:view_cart')
        if not product.product.status:
            messages.warning(request, f'{product.product.p_id.name} is not available')
            product.delete()
            return redirect('Cart:view_cart')
        if product.product.qty == 0:
            messages.warning(request, 'Out of stock!!')
            product.delete()
            return redirect('Cart:view_cart')
        if product.qty > product.product.qty:
            messages.warning(request, 'Quantity not available')
            product.delete()
            return redirect('Cart:view_cart')

    items_with_totals = []
    sub_total = 0

    # Calculate totals with offers
    for item in cart_items:
        # Calculate offer price
        offers = Product_Offers.objects.filter(product_id=item.product.pk).first()
        brand_offers = Brand_Offers.objects.filter(brand_id=item.product.p_id.brand.id).first()

        product_offer_price = item.product.price
        brand_offer_price = item.product.price

        # Apply product offer if available
        if offers:
            product_offer_price = item.product.price - (offers.offer_price / 100) * item.product.price

        # Apply brand offer if available
        if brand_offers:
            brand_offer_price = item.product.price - (brand_offers.offer_price / 100) * item.product.price

        # Choose the better offer
        if offers and brand_offers:
            if offers.offer_price >= brand_offers.offer_price:
                offer_price = product_offer_price
            else:
                offer_price = brand_offer_price
        elif offers:
            offer_price = product_offer_price
        elif brand_offers:
            offer_price = brand_offer_price
        else:
            offer_price = item.product.price

        # Calculate item total
        item_total = offer_price * item.qty
        items_with_totals.append((item, item_total))
        sub_total += item_total

        # Save the calculated price back to the item (optional)
        item.price = offer_price  # Save the price per unit (not total)
        item.save()

    # Apply delivery charges
    dlvry_charge = 0
    if sub_total < 50000:
        sub_total += 50
        dlvry_charge = 50

    context = {
        'addresses': address,
        'items_with_totals': items_with_totals,
        'subtotal': sub_total,
        'item': cart_items,
        'coupons': coupons,
        'final_price': final_price,
        'coupon_amount': coupon_amount,
        'coupon_code': coupon_code,
        'dlvry_charge': dlvry_charge,
    }
    return render(request, 'check_out/check_out.html', context)


#================================ coupon =================

        
    