from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import never_cache
from Product.models import Category,variant 
from Decorators.decorators import user_auth
from Product.views import is_staff
from django.db.models import Sum
from Brands.models import Brand 
from Order.models import Order_item, Order
from django.utils.timezone import now, timedelta
import json
from django.http import JsonResponse
from django.core import serializers

@never_cache
def user_home(request):
    products=variant.objects.all()
    context={'products':products}
    return render(request,"home_page/index.html",context)


@user_auth
@user_passes_test(is_staff,'Accounts:admin_login')
@login_required(login_url='Accounts:admin_login')
@never_cache
def admin_home(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('Accounts:admin_login')
    filter_option = request.GET.get('filter', 'daily')  
    today = now().date()
    
    orders = Order.objects.none()  # Default empty QuerySet
    
    if filter_option == 'daily':
        orders = Order.objects.filter(created_at__date=today)
    elif filter_option == 'weekly':
        week_ago = today - timedelta(days=7)
        orders = Order.objects.filter(created_at__date__gte=week_ago)
    elif filter_option == 'monthly':
        month_ago = today - timedelta(days=30)
        orders = Order.objects.filter(created_at__date__gte=month_ago)
    elif filter_option == 'yearly':
        year_ago = today - timedelta(days=365)
        orders = Order.objects.filter(created_at__date__gte=year_ago)
    elif filter_option == 'custom':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            orders = Order.objects.filter(created_at__date__range=[start_date, end_date])
    
    # Convert the date to string format
    sales_data = list(
        orders.values('created_at__date')
        .annotate(total_sales=Sum('total_price'))
        .order_by('created_at__date')
    )
    
    # Format dates to strings
    for item in sales_data:
        item['created_at__date'] = item['created_at__date'].strftime('%Y-%m-%d')

    top_products = (
        variant.objects
        .filter(order_item__status='Delivered')
        .annotate(total_sold=Sum('order_item__qty'))
        .order_by('-total_sold')[:10]
    )
    top_brands = (
        Brand.objects
        .filter(product__variant__order_item__status='Delivered')
        .annotate(total_quantity=Sum('product__variant__order_item__qty'))
        .order_by('-total_quantity')
    )[:10]
    
    top_categories = (
        Category.objects
        .filter(Product__variant__order_item__status='Delivered')
        .annotate(total_quantity=Sum('Product__variant__qty'))
        .order_by('-total_quantity')
    )[:10]
    
    total_sales = Order_item.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum']
    order_count = Order_item.objects.filter(status='Delivered').count()

    context = {
        'top_products': top_products,
        'top_brands': top_brands,
        'top_categories': top_categories,
        'total_sales': total_sales,
        'order_count': order_count,
        'sales_data': json.dumps(sales_data)  # Make sure sales_data is JSON serializable
    }
    
    return render(request, "admin_home/index.html", context)

     
