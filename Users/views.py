
from django.shortcuts import render,get_object_or_404,redirect
from Accounts.models import CustomUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Decorators.decorators import user_auth
from Product.views import is_staff
from .models import Address
from django.contrib import messages
import re
from django.http import JsonResponse

@login_required(login_url='Accounts:admin_login')
@never_cache
@user_passes_test(is_staff,'Accounts:admin_login')
def users(request):
    users=CustomUser.objects.filter(is_superuser=False)
    return render(request,'users/user_list.html',{'users':users})

def block(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_active = not user.is_active
    user.save()
    return redirect('Users:users')


#--------------------- user profile --------------------------------
@user_auth
@login_required(login_url='Accounts:user_login')
@never_cache
def user_profile(request):
    user_obj=0
    if request.user.is_authenticated and not request.user.is_staff:
   
        user_obj=CustomUser.objects.get(username=request.user)
    else:
       
        return redirect('Accounts:user_login')
    context={'user_obj':user_obj}
    return render(request,'user_profile/user_profile.html',context)

#========================== address ================================
@user_auth
@login_required(login_url='Accounts:user_login')
@never_cache
def all_address(request):
    user=request.user
    address=Address.objects.filter(user_id=user)
    context={'addresses':address}
    return render(request,'user_profile/all_address.html',context)
@user_auth
@login_required(login_url='Accounts:user_login')
def new_address(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name').strip()
        state = request.POST.get('state').strip()
        pincode = request.POST.get('pincode').strip()
        city = request.POST.get('city').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        landmark = request.POST.get('landmark').strip()


        # Regex patterns for validation
        name_pattern = re.compile(r'^[a-zA-Z\s]+$')
        state_pattern = re.compile(r'^[a-zA-Z\s]+$')
        city_pattern = re.compile(r'^[a-zA-Z\s]+$')

        # Validations
        if not name:
            messages.error(request, "Name is required.")
        elif not name_pattern.match(name):
            messages.error(request, "Name should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not state:
            messages.error(request, "State is required.")
        elif not state_pattern.match(state):
            messages.error(request, "State should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not pincode or not pincode.isdigit() or len(pincode) != 6:
            messages.error(request, "Please enter a valid 6-digit pincode.")
        elif not city:
            messages.error(request, "City is required.")
        elif not city_pattern.match(city):
            messages.error(request, "City should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not email or '@' not in email:
            messages.error(request, "Please enter a valid email address.")
        elif not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number.")
        elif not address:
            messages.error(request, "Address is required.")
        else:
            # Create a new address instance and save it if all validations pass
            address_instance = Address(
                user=user,
                name=name,
                state=state,
                pincode=pincode,
                city=city,
                email=email,
                phone_no=phone,
                address=address,
                landmark=landmark
            )
            address_instance.save()
            messages.success(request, "Address added successfully!")
            return redirect('Users:all_address')
        
    return render(request, 'user_profile/address.html')

@user_auth
@login_required(login_url='Accounts:user_login')
def edit_address(request, id):
    user_address = get_object_or_404(Address, id=id)
    context = {'address': user_address}

    if request.method == 'POST':
        name = request.POST.get('name').strip()
        state = request.POST.get('state').strip()
        pincode = request.POST.get('pincode').strip()
        city = request.POST.get('city').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        landmark = request.POST.get('landmark').strip()

        # Regex patterns for validation
        name_pattern = re.compile(r'^[a-zA-Z\s]+$')
        state_pattern = re.compile(r'^[a-zA-Z\s]+$')
        city_pattern = re.compile(r'^[a-zA-Z\s]+$')

        # Validations
        if not name:
            messages.error(request, "Name is required.")
        elif not name_pattern.match(name):
            messages.error(request, "Name should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not state:
            messages.error(request, "State is required.")
        elif not state_pattern.match(state):
            messages.error(request, "State should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not pincode or not pincode.isdigit() or len(pincode) != 6:
            messages.error(request, "Please enter a valid 6-digit pincode.")
        elif not city:
            messages.error(request, "City is required.")
        elif not city_pattern.match(city):
            messages.error(request, "City should only contain letters and spaces, with no continuous spaces or special characters.")
        elif not email or '@' not in email:
            messages.error(request, "Please enter a valid email address.")
        elif not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Please enter a valid 10-digit phone number.")
        elif not address:
            messages.error(request, "Address is required.")
        else:
            # Update the address instance if all validations pass
            user_address.name = name
            user_address.state = state
            user_address.pincode = pincode
            user_address.city = city
            user_address.email = email
            user_address.phone_no = phone
            user_address.address = address
            user_address.landmark = landmark

            user_address.save()
            messages.success(request, "Address updated successfully!")
            return redirect('Users:all_address')

    return render(request, 'user_profile/edit_address.html', context)

@login_required(login_url='Accounts:user_login')
def delete_address(request,id):
    address_id = get_object_or_404(Address,id = id)
    address_id.delete()
    return redirect('Users:all_address')

#================================== edit details ===============================
@user_auth
@login_required(login_url='Accounts:user_login')
@never_cache
def edit_details(request):
    user=get_object_or_404(CustomUser,id=request.user.id)
    if request.method == 'POST':
        fname=request.POST.get('name')
        lname=request.POST.get('lname')
        phone=request.POST.get('phone')
       
        user.first_name=fname
        user.last_name=lname
        user.phone_no=phone
        
        user.save()
    return redirect('Users:user_profile')


#================================== add new address in the checkout ==================

# Patterns for name, state, and city validation
name_pattern = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")  # Only letters and single spaces allowed
state_pattern = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")  # Similar to name pattern
city_pattern = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")  # Similar to name pattern

@user_auth
@login_required(login_url='Accounts:user_login')
def add_new_address(request):
    if request.method == "POST":
        user = request.user  # Assuming the user is logged in
        name = request.POST.get('name')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')

        # Validations
        if not name:
            return JsonResponse({'status': 'error', 'message': "Name is required."}, status=400)
        elif not name_pattern.match(name):
            return JsonResponse({'status': 'error', 'message': "Name should only contain letters and spaces, with no continuous spaces or special characters."}, status=400)
        
        if not state:
            return JsonResponse({'status': 'error', 'message': "State is required."}, status=400)
        elif not state_pattern.match(state):
            return JsonResponse({'status': 'error', 'message': "State should only contain letters and spaces, with no continuous spaces or special characters."}, status=400)
        
        if not pincode or not pincode.isdigit() or len(pincode) != 6:
            return JsonResponse({'status': 'error', 'message': "Please enter a valid 6-digit pincode."}, status=400)
        
        if not city:
            return JsonResponse({'status': 'error', 'message': "City is required."}, status=400)
        elif not city_pattern.match(city):
            return JsonResponse({'status': 'error', 'message': "City should only contain letters and spaces, with no continuous spaces or special characters."}, status=400)
        
        if not email or '@' not in email:
            return JsonResponse({'status': 'error', 'message': "Please enter a valid email address."}, status=400)
        
        if not phone_no or not phone_no.isdigit() or len(phone_no) != 10:
            return JsonResponse({'status': 'error', 'message': "Please enter a valid 10-digit phone number."}, status=400)
        
        if not address:
            return JsonResponse({'status': 'error', 'message': "Address is required."}, status=400)

        # If all validations pass, create a new Address instance
        Address.objects.create(
            user=user,
            name=name,
            state=state,
            pincode=pincode,
            city=city,
            email=email,
            phone_no=phone_no,
            address=address,
            landmark=landmark
        )

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
