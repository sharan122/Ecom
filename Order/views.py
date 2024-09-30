from django.shortcuts import render,get_object_or_404,redirect
from Users.models import Address
from Cart.models import Cart,Cart_item
from Product.models import variant
from Order.models import Shippment_address,Order,Order_item
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from Decorators.decorators import user_auth
from django.contrib import messages
from Wallet.models import Wallet,Transaction
from django.http import JsonResponse
from Coupons.models import Coupons,Coupon_users
import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum
import razorpay
from django.conf import settings
import json 
import pdfkit
from django.template.loader import render_to_string  

# Create your views here.

@user_auth
@login_required(login_url='Accounts:user_login')
def place_order(req):
    if req.method == "POST":
        user_id = req.user
        cart_id = get_object_or_404(Cart, user_id=user_id)
        cart_items = Cart_item.objects.filter(cart=cart_id)
        total_price = sum(item.price * item.qty for item in cart_items)
  
        coupon_amount = req.session.get('coupon_amount',0)
        total_price -= coupon_amount
        
        if total_price < 50000:
            total_price+=50
        
        for product in cart_items:
            if not product.product.p_id.brand.status:
                messages.warning(req, f'Sorry, {product.product.p_id.brand.brand_name} products are not available')
                product.delete()
                return redirect('Cart:view_cart')
            if not product.product.status:
                product.delete()
                messages.warning(req, 'Product not available')
                return redirect('Cart:view_cart')
            if product.product.qty == 0:
                product.delete()
                messages.warning(req, 'Out of stock!')
                return redirect('Cart:view_cart')
            if product.qty > product.product.qty:
                product.delete()
                messages.warning(req, 'Quantity not available')
                return redirect('Cart:view_cart')

        
        a = req.POST.get('existing_address_id')
        if a:
            user_address = Address.objects.filter(id=a)
            for item in user_address:
                if not item.status:
                    messages.warning(req, 'Address is not valid')
                    return redirect('Cart:check_out')
                else:
                    address_id = Shippment_address.objects.create(
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
           
            name = req.POST.get('name')
            state = req.POST.get('state')
            pincode = req.POST.get('pincode')
            city = req.POST.get('city')
            email = req.POST.get('email')
            phone_no = req.POST.get('phone')
            address = req.POST.get('address')
            landmark = req.POST.get('landmark')
            if not name or not state or not pincode or not city or not email or not phone_no or not address:
                messages.warning(req, 'Please fill all the fields')
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
            address_id = Shippment_address(
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



              

        payment_method = req.POST.get('payment_method')

        if payment_method == 'Razorpay':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment_data = {
                "amount": int(total_price * 100),  # Amount in paise
                "currency": "INR",
                "payment_capture": 1
            }
            try:
                payment = client.order.create(data=payment_data)
            except razorpay.errors.BadRequestError:
                messages.error(req, 'Error creating Razorpay order. Please try again.')
                return redirect('Cart:check_out')

            order = Order.objects.create(
                user_id=user_id,
                address_id=address_id,
                total_price = total_price,
                payment_type = 'Razorpay',
                status ="Payment Failed",
                razorpay_order_id = payment['id']
            )
            for item in cart_items:
                product = variant.objects.get(id=item.product.id)
                Order_item.objects.create(
                    order_id=order,
                    product_id=product,
                    qty=item.qty,
                    total_price=(item.price * item.qty),
                    status="Payment Failed"
                    
                )
            cart_items.delete()
            req.session['pending_order_id'] = order.id

            return JsonResponse({
                'order_id': payment['id'],
                'amount': payment_data['amount'],
                'currency': payment_data['currency'],
                'key': settings.RAZORPAY_KEY_ID,
            })

        elif payment_method == 'COD':
            coupon_value = 0
            if coupon_amount > 0:
                coupon_value = req.session.get('coupon_amount')
            order = Order.objects.create(
                user_id=user_id,
                address_id=address_id,
                total_price=total_price,
                payment_type='COD',
                status="Order Placed",
                coupon_amount = coupon_value
                
                
            )
            for item in cart_items:
                product = variant.objects.get(id=item.product.id)
                Order_item.objects.create(
                    order_id=order,
                    product_id=product,
                    qty=item.qty,
                    total_price=(item.price * item.qty),
                    status="Order Placed",
                    
                    
                )
                
            if coupon_amount > 0:
                coupon_instance = Coupons.objects.get(coupon_code=req.session.get('coupon_code'))
                Coupon_users.objects.create(user_id= req.user,coupon_code=coupon_instance)
                req.session.pop('coupon_code', None)
                req.session.pop('final_price', None)
                req.session.pop('coupon_amount', None)
                

            cart_items.delete()
            req.session['pending_order_id'] = order.id
            return JsonResponse({
                'message': 'Order placed successfully.'
            })

    return redirect('Cart:check_out')



def payment_success(req):
    if req.method == "POST":
        cart_id = get_object_or_404(Cart, user_id=req.user)
        cart_items = Cart_item.objects.filter(cart=cart_id)
        
        payment_data = json.loads(req.body.decode('utf-8'))
        params_dict = {
            'razorpay_order_id': payment_data.get('razorpay_order_id'),
            'razorpay_payment_id': payment_data.get('razorpay_payment_id'),
            'razorpay_signature': payment_data.get('razorpay_signature')
        }

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        

        try:
            client.utility.verify_payment_signature(params_dict)
            order_id = req.session.get('pending_order_id')
            if order_id:
                order = Order.objects.get(id=order_id)
                order.status = "Order Placed"
                order.coupon_amount = req.session.get('coupon_amount')
                order.save()

                order_items = Order_item.objects.filter(order_id=order)
                for item in order_items:
                    item.status = "Order Placed"
                    item.save()
                    product = item.product_id
                    product.qty -= item.qty
                    product.save()
                
                
                cart_items.delete()
            coupon_amount = req.session.get('final_price',0)
            if coupon_amount > 0:
                coupon_instance = Coupons.objects.get(coupon_code=req.session.get('coupon_code'))
                Coupon_users.objects.create(user_id= req.user,coupon_code=coupon_instance)
                del req.session['pending_order_id']
                req.session.pop('coupon_code', None)
                req.session.pop('final_price', None)
                req.session.pop('coupon_amount', None)
                
                return JsonResponse({
                    'message': 'Razorpay order created successfully.'
                })
            else:
                messages.error(req, 'No pending order found.')
                return redirect('Cart:view_cart')

        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment verification failed")
    
    return render(req, "check_out/success.html")
#=================================== Retry payment ========================
def retry_payment(req, order_id):
    order = get_object_or_404(Order, id=order_id, user_id=req.user, status="Payment Failed")
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_data = {
        "amount": int(order.total_price * 100),  # Amount in paise
        "currency": "INR",
        "payment_capture": 1
    }
    
    try:
        payment = client.order.create(data=payment_data)
    except razorpay.errors.BadRequestError:
        messages.error(req, 'Error creating Razorpay order. Please try again.')
        return redirect('Order:order_details', order_id=order.id)

    # Update the order with the new Razorpay order ID
    order.razorpay_order_id = payment['id']
    order.save()
    coupon_amount = req.session.get('final_price',0)
    if coupon_amount > 0:
        req.session.pop('coupon_code', None)
        req.session.pop('final_price', None)
        req.session.pop('coupon_amount', None)
    return JsonResponse({
        'order_id': payment['id'],
        'amount': payment_data['amount'],
        'currency': payment_data['currency'],
        'key': settings.RAZORPAY_KEY_ID,
    })

#===================================== verify payment =================================

def verify_payment(req):
    if req.method == 'POST':
        data = req.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            # Payment is verified, update the order status
            order.status = 'Order Placed'
            order.save()

            order_items = Order_item.objects.filter(order_id=order)
            for item in order_items:
                item.status = "Order Placed"
                item.save()

            return JsonResponse({'status': 'Payment verified successfully'})
        
        except razorpay.errors.SignatureVerificationError:
            # Payment failed due to invalid signature
            order.status = 'Payment Failed'
            order.save()
            return JsonResponse({'status': 'Payment verification failed'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
#=================================== apply coupon =====================================

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')

        
        try:
            coupon = Coupons.objects.get(coupon_code=code)
        except Coupons.DoesNotExist:
            return JsonResponse({'error': 'Invalid coupon code.'}, status=400)
        
        if Coupon_users.objects.filter(user_id=request.user, coupon_code=coupon).exists():
            return JsonResponse({'error': 'You have already used this coupon.'})
        
        
        # Ensure the coupon is active
        if not coupon.status:

            return JsonResponse({'error': 'This coupon is no longer active.'}, status=400)

        # Ensure the coupon hasn't expired
        if coupon.expiry < timezone.now().date():

            return JsonResponse({'error': 'This coupon has expired.'}, status=400)
        
        # Get the user's cart and cart items
        cart = get_object_or_404(Cart, user_id=request.user)
        cart_items = Cart_item.objects.filter(cart=cart)
        
        # Calculate total price of the cart items
        total_price = sum(item.price * item.qty for item in cart_items)

        

        if total_price < coupon.min_amount:

            return JsonResponse({'error': f'Your order must be at least ₹{coupon.min_amount} to use this coupon.'}, status=400)


        if total_price > coupon.max_amount:
     
            return JsonResponse({'error': f'Your order must be under ₹{coupon.max_amount} to use this coupon.'}, status=400)

   
        discount = (coupon.percentage / 100) * total_price
        discounted_total = total_price - discount
        request.session['coupon_amount'] = discount
        request.session['final_price'] = discounted_total
        request.session['coupon_code'] = code
        

        # Return success response with the discount and updated price
        return JsonResponse({
            'success': True,
            'discount': f'₹{discount:.2f}',
            'discounted_total': f'{discounted_total:.2f}'
        })
    
    return JsonResponse({'error': 'Invalid request.'}, status=400)
     
#============================= remove coupon ===============================

def remove_coupon(request):
    if request.method == 'POST':
        # Check if the coupon details are present in the session
        if 'coupon_code' in request.session:
            # Remove coupon-related session data
            del request.session['coupon_code']
            del request.session['coupon_amount']
            del request.session['final_price']
            
            # Return a success message
            return JsonResponse({
                'success': True,
                'message': 'Coupon removed successfully.'
            })
        else:
            return JsonResponse({'error': 'No coupon applied.'}, status=400)

    return JsonResponse({'error': 'Invalid request.'}, status=400)

#============================= admin order details =========================
@user_auth
@login_required(login_url='Accounts:user_login')
def order_list(req):
    # Base queryset
    orders = Order_item.objects.all().order_by('-id')

    start_date = req.GET.get('start_date')
    end_date = req.GET.get('end_date')
    filter_option = req.GET.get('filter_option')

    # Apply date filter based on filter_option
    if filter_option:
        if filter_option == "1_day":
            start_date = datetime.date.today() - datetime.timedelta(days=1)
        elif filter_option == "1_week":
            start_date = datetime.date.today() - datetime.timedelta(weeks=1)
        elif filter_option == "1_month":
            start_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today()

    # Apply date range filter
    if start_date:
        orders = orders.filter(order_id__created_at__gte=start_date)
    if end_date:
        orders = orders.filter(order_id__created_at__lte=end_date)

    # Calculate metrics based on the filtered queryset
    order_count = orders.filter(status='Delivered').count()
    total_delivered_price = orders.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_discount = Order.objects.filter(
        id__in=orders.values_list('order_id', flat=True),
        status='Order Placed'
    ).aggregate(Sum('coupon_amount'))['coupon_amount__sum'] or 0

    context = {
        'orders': orders,
        'start_date': start_date,
        'end_date': end_date,
        'filter_option': filter_option,
        'total_sales': total_delivered_price,
        'total_order': order_count,
        'total_discount': total_discount
    }

    if req.GET.get('download') == 'pdf':
        return generate_pdf('Order/order_pdf_template.html', context)

    return render(req, 'Order/order_list.html', context)

def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error occurred while generating PDF')
    return response


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
    
    items = Order_item.objects.get(id = id)
    current_item = items.id
    other_item = Order_item.objects.filter(order_id= items.order_id.pk)
    item_count=other_item.count()
    
    context = {
        'items':item,
        'other_item':other_item,
        'current_item':current_item,
        'item_count':item_count
    }
    
    return render(req,'user_profile/order_details.html',context)

#======================= order status =======================================

def order_status(req, id):
    item = get_object_or_404(Order_item, id=id)
    order_count = Order_item.objects.filter(order_id = item.order_id.pk).count()
    status = req.POST.get('status')
    item_price = item.total_price
    coupon_amount = item.order_id.coupon_amount or 0
    
    if status:
        
        if coupon_amount > 0:
            item_price -= coupon_amount/order_count
            

        if status == 'Return Accepted' or (status == 'Order Cancelled !' and item.order_id.payment_type == 'Razorpay'):
            
            user_wallet = get_object_or_404(Wallet, user_id=item.order_id.user_id.id)
            user_wallet.balance += int(item_price)  
            item.message = ' '
        
            user_wallet.save()
            

            user_transaction = Transaction.objects.create(
                wallet_id=user_wallet,
                Amount=item_price,
                message=f'{item.product_id.p_id.name} cancelled',
                transaction_type=item.order_id.payment_type
            )
        

        if status in ['Return Accepted', 'Order Cancelled !']:
            item.product_id.qty += item.qty
            item.product_id.save()
        

        item.status = status
        item.save()
    

    return redirect('Order:order_list')

#============================ cancel order =================================
@user_auth
@login_required(login_url='Accounts:user_login')
def cancel_order(req, id):
    item = Order_item.objects.get(id=id)
    items_count = Order_item.objects.filter(order_id=item.order_id.pk).count()
    item.status = "Order Cancelled !"
    coupon_amount = item.order_id.coupon_amount
    product_price = item.total_price
    
    if coupon_amount > 0:
        product_price -= coupon_amount/items_count  
        
    

    item.product_id.qty += item.qty
    item.order_id.total_price -= product_price
    

    if item.order_id.payment_type == 'Razorpay':
        user_wallet = get_object_or_404(Wallet, user_id=item.order_id.user_id.id)
        user_wallet.balance += int(product_price)
        user_wallet.save()
        
        user_transaction = Transaction.objects.create(
            wallet_id=user_wallet,
            Amount=product_price,
            message= f'{item.product_id.p_id.name} cancelled',
            transaction_type=item.order_id.payment_type
        )
    
    item.order_id.save()
    item.product_id.save()
    item.save()
    

    return redirect('Order:user_order_details', id=id)
#======================= request return ============================

def request_return(request,id):
    item = Order_item.objects.get(id=id)
    if item.status == 'Delivered':
        item.status = "Requested For Return"
        item.message = "Requested For Return"
        item.save()
    return redirect('Order:user_order_details', id=id)

#========================== suceess ===============================

def success(request):
    return render(request, "check_out/success.html")


#========================= Invoice ==================================

def generate_invoice(request, order_item_id):
    # Fetch the order item based on the ID
    order_item = Order_item.objects.get(id=order_item_id, status='Delivered')

    # Get the corresponding order details
    order = order_item.order_id
    
    # Render the HTML template for the invoice
    html = render_to_string('user_profile/invoice/invoice.html', {
        'order_item': order_item,
        'order': order,
        'invoice_number': order_item_id,
        'invoice_date': order.created_at.strftime('%Y-%m-%d'),
    })

    # Generate the PDF from the rendered HTML
    pdf = pdfkit.from_string(html, False)

    # Create the HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_item_id}.pdf"'

    return response
    
   

    
    
    
    
    