from django.shortcuts import render,get_object_or_404,redirect
from Users.models import Address
from Cart.models import Cart,Cart_item
from Product.models import variant
from Order.models import Shippment_address,Order,Order_item
from django.contrib.auth.decorators import login_required
from Decorators.decorators import user_auth
from django.contrib import messages


# Create your views here.
@user_auth
@login_required(login_url='Accounts:user_login')
def place_order(req):
    if req.method == "POST":
        user_id = req.user
        
        cart_id = get_object_or_404(Cart,user_id=user_id)
        cart_items = Cart_item.objects.filter(cart=cart_id)
        
        for product in cart_items:
            if product.product.p_id.brand.status == False:
                
                messages.warning(req,f'Sorry {product.product.p_id.brand.brand_name} products are not available')
                product.delete()
                return redirect('Cart:view_cart')
            if product.product.status == False  :
                product.delete()
                messages.warning(req,'Product not available')
                product.delete()
                return redirect('Cart:view_cart')
            if product.product.qty == 0  :
                product.delete()
                messages.warning(req,'Out of stock!!')
                return redirect('Cart:view_cart')
            if product.qty > product.product.qty:
                product.delete()
                messages.warning(req,'Quantity not availale')
                return redirect('Cart:view_cart')
            
        a = req.POST.get('existing_address_id')
        print(a)
        if a:
            user_address=Address.objects.filter(id =a)
            for item in user_address:
                if item.status == False:
                    messages.warning(req,'Addresss is not valid')
                    return redirect('Cart:check_out')
                else: 
                    address_id=Shippment_address.objects.create(
                    user=user_id,
                    name=item.name,
                    state=item.state,
                    pincode=item.pincode,
                    city=item.city,
                    email=item.email,
                    phone_no=item.phone_no,
                    address=item.address,
                    landmark=item.landmark,
       
            )
        else:
            name=req.POST.get('name')
            state=req.POST.get('state')
            pincode=req.POST.get('pincode')
            city=req.POST.get('city')
            email=req.POST.get('email')
            phone_no=req.POST.get('phone')
            address=req.POST.get('address')
            landmark=req.POST.get('landmark')
            if not name or not state or not pincode or not city or not email or not phone_no or not address:
                messages.warning(req,'Please fill all the feilds')
                return redirect('Cart:check_out')
            save_address = Address(
                
                user=user_id,
                name=name,
                state=state,
                pincode=pincode,
                city=city,
                email=email,
                phone_no=phone_no,
                address=address,
                landmark=landmark,   
            )
            save_address.save()
            address_id=Shippment_address(
                user=user_id,
                name=name,
                state=state,
                pincode=pincode,
                city=city,
                email=email,
                phone_no=phone_no,
                address=address,
                landmark=landmark,   
            )
            address_id.save()
        
    order = Order.objects.create(
        user_id = user_id,
        address_id = address_id,
        total_price = sum(item.product.price * item.qty for item in cart_items),
        payment_type = req.POST.get('payment_method'),
        status = "Order Placed"
    )
    
    
    for item in cart_items:
            product = variant.objects.get(id=item.product.id)
            Order_item.objects.create(
                order_id=order,
                product_id=product,
                qty=item.qty,
                total_price=product.price * item.qty,
                status="Order Placed"
            )
            product.qty-=item.qty
            product.save()
    cart_items.delete()
    return render(req,"check_out/success.html")      

#============================= admin order details =========================
@user_auth
@login_required(login_url='Accounts:user_login')
def order_list(req):
    orders=Order_item.objects.all().order_by('-id')
    context={
        'orders':orders
    }
    return render(req,'Order/order_list.html',context)

#=========================== user order ===============================

def user_order(req):
    user_id = req.user
    order_id = Order.objects.filter(user_id=user_id).order_by('-id')
    context = {
        'items':order_id
    }
    return render(req,'user_profile/user_order.html',context)

#========================== order items ==============================
@user_auth
@login_required(login_url='Accounts:user_login')
def order_items(req, id):
    items =  Order_item.objects.filter(order_id = id)
    context = {
        'items' : items
    }
    
    return render(req,'user_profile/order_items.html',context)

#==============================user order details =========================
@user_auth
@login_required(login_url='Accounts:user_login')
def user_order_details(req,id):
    item = Order_item.objects.filter(id = id)
    context = {
        'items':item
    }
    
    return render(req,'user_profile/order_details.html',context)

#============================ cancel order =================================
@user_auth
@login_required(login_url='Accounts:user_login')
def cancel_order(req,id):
    item = Order_item.objects.get(id=id)
    item.status = "Order Cancelled !"
    item.product_id.qty += item.qty
    item.order_id.total_price-= item.total_price
    item.order_id.save()
    item.product_id.save()
    item.save()
    return redirect('Order:user_order_details',id=id)

#======================= order status =======================================

def order_status(req, id):
    item = get_object_or_404(Order_item, id=id)
    status = req.POST.get('status')
    if status:
        item.status = status
        item.save()
    return redirect('Order:order_list')
    
    
    
    
    