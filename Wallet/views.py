from django.shortcuts import render,get_object_or_404
from Wallet.models import Transaction,Wallet

# Create your views here.
def transactions(request):
    wallet = get_object_or_404(Wallet,user_id = request.user)
    user_transactons = Transaction.objects.filter(wallet_id = wallet).order_by('-id')
    context = {
        'transactions':user_transactons,
        'balance':wallet.balance
        }
    return render(request,'user_profile/wallet/wallet.html',context)