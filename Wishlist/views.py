from django.shortcuts import render, redirect,get_object_or_404
from Wishlist.models import Wishlist
from Product.models import variant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='Accounts:user_login')
def wishlist(request):
    products = Wishlist.objects.filter(user= request.user.id)
    context={
        'products':products
    }
    return render(request,'user_profile/wishlist/wishlist.html',context)

@login_required(login_url='Accounts:user_login')
def add_wishlist(request, id):
    user = request.user
    product = get_object_or_404(variant, id=id)
    already_exists = Wishlist.objects.filter(user=user, product=product).exists()

    if not already_exists:
        Wishlist.objects.create(user=user, product=product)
        message = "Item added to wishlist!"
        success = True
    else:
        message = "Item already in wishlist."
        success = False

    return JsonResponse({'success': success, 'message': message})

@login_required(login_url='Accounts:user_login')
def remove_wishlist(request,id):
    item = get_object_or_404(Wishlist,product = id)
    item.delete()
    return redirect('Wishlist:wishlist')
    