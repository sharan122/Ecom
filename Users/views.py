from django.shortcuts import render,get_object_or_404,redirect
from Accounts.models import CustomUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Accounts.models import CustomUser
from Decorators.decorators import user_auth
from Product.views import is_staff

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
def user_profile(request):
    user_obj=0
    if request.user.is_authenticated and not request.user.is_staff:
   
        user_obj=CustomUser.objects.get(username=request.user)
    else:
       
        return redirect('Accounts:user_login')
    context={'user_obj':user_obj}
    return render(request,'user_profile/user_profile.html',context)