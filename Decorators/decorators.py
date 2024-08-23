from django.shortcuts import redirect

def user_auth(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_active:
            return redirect('Accounts:user_login')
        return func(request, *args, **kwargs)
    return wrapper