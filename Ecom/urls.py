"""
URL configuration for Ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admins/', admin.site.urls),
    path('',include('Home.urls')),
    path('login/',include('Accounts.urls')),
    path('product/',include('Product.urls')),
    path('users/',include('Users.urls')),
    path('accounts/', include('allauth.urls')),
    path('brands/',include('Brands.urls')),
    path('cart/', include('Cart.urls')),
    path('order/', include('Order.urls')),
    path('offers/', include('Offers.urls')),
    path('wishlist/', include('Wishlist.urls')),
    path('coupon/', include('Coupons.urls')),
    path('wallet/', include('Wallet.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)