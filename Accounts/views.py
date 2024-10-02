from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import  HttpResponseRedirect
from .models import CustomUser 
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime
import re
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.conf import settings


# user login view
@never_cache
def user_login(request):
    if request.session.session_key:
        return redirect('Home:user_home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

       
        if not email or not password:
            messages.warning(request, "Email and password are required.")
            return HttpResponseRedirect(request.path_info)

      
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.warning(request, "Please enter a valid email address.")
            return HttpResponseRedirect(request.path_info)

       
        user_obj = CustomUser.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, "Account not found.")
            return HttpResponseRedirect(request.path_info)

      
        for obj in user_obj:
            if not obj.is_active:
                messages.error(request, "Entry Restricted! Your account is inactive.")
                return HttpResponseRedirect(request.path_info)

       
        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('Home:user_home')
        else:
           
            messages.warning(request, "Incorrect password.")
            return HttpResponseRedirect(request.path_info)
    
    return render(request, "login_page/login_page.html")
#---------------------SignUp and otp-----------------------------------
def generate_otp():
    return random.randint(100000, 999999)

# User signup view
@never_cache
def user_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email')
        phone = request.POST.get('phone').strip()
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')

        # Validate first and last names
        if not first_name or not last_name:
            messages.error(request, "First name and last name cannot be empty.")
            return HttpResponseRedirect(request.path_info)
        
        if first_name == '' or last_name == '':
            messages.error(request, "First name and last name cannot contain only spaces.")
            return HttpResponseRedirect(request.path_info)
        
        # Validate phone number
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Phone number must be 10 digits long and contain only numbers.")
            return HttpResponseRedirect(request.path_info)

        # Validate password
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messages.error(request, "Password must be at least 8 characters long and include a mix of uppercase letters, lowercase letters, numbers, and special characters.")
            return HttpResponseRedirect(request.path_info)
        
        if password != c_password:
            messages.error(request, "Both Passwords Should Be Same!!!")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = CustomUser.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, "User Already Exists")
            return HttpResponseRedirect(request.path_info)
        
        otp = generate_otp()
        otp_expiry = timezone.now() + timedelta(minutes=3)
        
        # Store OTP and expiry time in the session
        request.session['otp'] = otp
        request.session['otp_expiry'] = otp_expiry.isoformat()
        request.session['email'] = email
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['phone'] = phone
        request.session['password'] = password
        
        # Send OTP to email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'your_email@example.com',
            [email],
            fail_silently=False,
        )
        
        # Redirect to OTP verification page
        return redirect('Accounts:verify_otp')
    
    return render(request, "signup_page/signup_page.html")


def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        otp_expiry_str = request.session.get('otp_expiry', None)

        if otp_expiry_str:
            otp_expiry = parse_datetime(otp_expiry_str)
        
        if stored_otp and otp_expiry and timezone.now() < otp_expiry:
            if str(stored_otp) == str(input_otp):
                user = CustomUser.objects.create_user(
                    username=request.session['email'],
                    first_name=request.session['first_name'],
                    last_name=request.session['last_name'],
                    email=request.session['email'],
                    phone_no=request.session['phone'],
                    password=request.session['password'],
                    is_active=True,
                    signup_method = 'default'
                )
                user.save()
                request.session.flush()
                messages.success(request, "Account created successfully!")
                return redirect('Accounts:user_login')
            else:
                messages.error(request, "Invalid OTP")
        else:
            messages.error(request, "OTP expired or invalid. Please try again.")
            
        return redirect(request.path_info)
    
    otp_expiry = request.session.get('otp_expiry', None)
    return render(request, "verify_otp_page/verify_otp_page.html", {'otp_expiry': otp_expiry})


def resend_otp(request):
    if 'email' not in request.session:
        # If the session does not have email info, redirect to signup or some other page
        messages.error(request, "Session expired. Please sign up again.")
        return redirect('Accounts:user_signup')
    
    otp = generate_otp()
    otp_expiry = timezone.now() + timedelta(minutes=1)
    
    request.session['otp'] = otp
    request.session['otp_expiry'] = otp_expiry.isoformat()

    send_mail(
        'Your OTP Code',
        f'Your new OTP code is {otp}',
        'your_email@example.com',
        [request.session['email']],
        fail_silently=False,
    )

    messages.success(request, "OTP has been resent.")
    return redirect('Accounts:verify_otp')




#admin signup view
def admin_login(request):
  
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        admin_obj=authenticate(username=username,password=password)
        if admin_obj is not None and admin_obj.is_staff:
            login(request, admin_obj)
            return redirect('Home:admin_home')
          
        else:
            messages.success(request,"You are not an ADMIN!!!")
            return HttpResponseRedirect(request.path_info)
    return render(request,"login_page/admin_login.html")
     
     

def logout_user(request):
    logout(request)
    return redirect('Accounts:user_login')

def logout_admin(request):
    logout(request)
    return redirect('Accounts:admin_login')



@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please try again.')
        elif new_password != confirm_password:
            messages.error(request, 'The new passwords do not match. Please try again.')
        elif len(new_password) < 8:
            messages.error(request, 'The new password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('Accounts:change_password')

    return render(request, 'user_profile/change_password.html')

def set_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('con_password')
        if len(new_password) < 8:
            messages.error(request, 'The new password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'The new passwords do not match. Please try again.')
        
        request.user.set_password(new_password)
        request.user.signup_method='default'
        request.user.username= request.user.email
        request.user.save()
        messages.success(request, 'Your password has been successfully updated!') 
        return redirect('Accounts:set_password')
    return render(request, 'user_profile/set_password.html')


#=========================== forgot password =========================================

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('Accounts:password_reset_confirm', args=[uid, token])
            )
            context = {
                'user': user,
                'reset_link': reset_link,
            }
            subject = 'Password Reset Requested'
            message = render_to_string('forgot_password/password_reset_email.html', context)
            send_mail(subject, message,settings.DEFAULT_FROM_EMAIL,[email])
            return redirect('Accounts:password_reset_done')
        else:
            return HttpResponse("User with this email does not exist.")
    return render(request, 'forgot_password/password_reset_form.html')


def password_reset_confirm(request, uidb64, token):
    UserModel = get_user_model()
    uid = urlsafe_base64_decode(uidb64).decode()
    user = UserModel.objects.get(pk=uid)
    
    if default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return redirect('Accounts:password_reset_complete')
            else:
                return HttpResponse("Passwords do not match.")
        return render(request, 'forgot_password/password_reset_confirm.html')
    else:
        return HttpResponse("Invalid token.")