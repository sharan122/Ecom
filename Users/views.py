from django.shortcuts import render,get_object_or_404,redirect
from Accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required(login_url='Accounts/admin_login/')
@never_cache
def users(request):
    users=CustomUser.objects.filter(is_superuser=False)
    return render(request,'users/user_list.html',{'users':users})

def block(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_active = not user.is_active
    user.save()
    return redirect('Users:users')