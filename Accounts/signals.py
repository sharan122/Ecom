from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from Wallet.models import Wallet

@receiver(user_logged_in)
def create_wallet_on_login(sender, user, request, **kwargs):
    if not Wallet.objects.filter(user_id=user.id).exists():  
        Wallet.objects.create(user_id=user)
