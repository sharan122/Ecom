import json
from django.shortcuts import render,get_object_or_404,redirect
from Coupons.models import Coupons
import random
import string
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from datetime import datetime
from Cart.models import Cart,Cart_item
from django.http import JsonResponse
from datetime import date
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.
def is_staff(user):
    return user.is_staff


def generate_coupon_code(length=6):
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choices(letters_and_digits, k=length))

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def add_coupon(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        percentage = request.POST.get('percentage')
        max_amount = request.POST.get('max_amount')
        min_amount = request.POST.get('min_amount')
        
        expiry = request.POST.get('expiry')
        
        
        errors = False

        
        if not description:
            messages.error(request, "Description is required.")
            errors = True

       
        try:
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                messages.error(request, "Percentage must be between 1 and 100.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Percentage must be a valid number.")
            errors = True

       
        try:
            max_amount = float(max_amount)
            if max_amount <= 0:
                messages.error(request, "Max amount must be a positive number.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Max amount must be a valid number.")
            errors = True

        
        try:
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
            if expiry_date < datetime.now():
                messages.error(request, "Expiry date must be in the future.")
                errors = True
        except ValueError:
            messages.error(request, "Expiry date must be a valid date (YYYY-MM-DD).")
            errors = True

        # If no errors, create the coupon
        if not errors:
            coupon_code = generate_coupon_code()
            Coupons.objects.create(
                description=description,
                coupon_code=coupon_code,
                percentage=percentage,
                max_amount=max_amount,
                min_amount=min_amount,
                expiry=expiry_date
            )
            messages.success(request, "Coupon created successfully!")
            return redirect('Coupons:all_coupond')

    return render(request, 'coupon/coupon.html')

#========================= show all coupons =====================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def all_coupond(request):
    coupons = Coupons.objects.all()
    context = {
        'coupons':coupons
    }
    return render(request,'coupon/coupon_list.html',context)
 #================================= edit coupon ================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def edit_coupon(request, id):
    coupon = get_object_or_404(Coupons, id=id)

    if request.method == 'POST':
        description = request.POST.get('description')
        percentage = request.POST.get('percentage')
        max_amount = request.POST.get('max_amount')
        min_amount = request.POST.get('min_amount')
        expiry = request.POST.get('expiry')

        # Validation
        errors = False

        # Validate description
        if not description:
            messages.error(request, "Description is required.")
            errors = True

        # Validate percentage
        try:
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                messages.error(request, "Percentage must be between 1 and 100.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Percentage must be a valid number.")
            errors = True

        # Validate max amount
        try:
            max_amount = float(max_amount)
            if max_amount <= 0:
                messages.error(request, "Max amount must be a positive number.")
                errors = True
        except (ValueError, TypeError):
            messages.error(request, "Max amount must be a valid number.")
            errors = True

        # Validate expiry date
        try:
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
            if expiry_date < datetime.now():
                messages.error(request, "Expiry date must be in the future.")
                errors = True
        except ValueError:
            messages.error(request, "Expiry date must be a valid date (YYYY-MM-DD).")
            errors = True

        # If no errors, update the coupon
        if not errors:
            coupon.description = description
            coupon.percentage = percentage
            coupon.max_amount = max_amount
            coupon.min_amount = min_amount
            coupon.expiry = expiry_date
            coupon.save()

            messages.success(request, "Coupon updated successfully!")
            return redirect('Coupons:all_coupond')

    # Handle GET request
    context = {
        'coupon': coupon
    }
    return render(request, 'coupon/coupon.html', context)
    
#=========================== remove coupon ===================================
@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def remove_coupon(request,id):
    coupon = get_object_or_404(Coupons,id = id)
    coupon.delete()
    return redirect('Coupons:all_coupond')

    
#================================ Apply coupon js ===============


def apply_coupon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON data
            coupon_code = data.get('coupon_code')  # Get the coupon code from JSON
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'})

        if coupon_code:
            try:
                coupon = Coupons.objects.get(coupon_code=coupon_code, status=True, expiry__gte=date.today())
                return JsonResponse({
                    'success': True,
                    'percentage': coupon.percentage,
                    'max_amount': coupon.max_amount
                })
            except Coupons.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid or expired coupon code'})
        else:
            return JsonResponse({'success': False, 'message': 'No coupon code provided'})
#=================================== checkout listing =========================================


    
    
    
    
        
        
        