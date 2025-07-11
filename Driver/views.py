from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_driver(user):
    if user.is_superuser:
        return True
    print("Authenticated:", user.is_authenticated)
    print("User:", user)
    print("Groups:", list(user.groups.values_list('name', flat=True)))
    return user.groups.filter(name__iexact='Driver').exists()

@login_required(login_url='/accounts/login/')
@user_passes_test(is_driver, login_url='/accounts/unauthorized/')
def driver(request): 
    return render(request, "driverinterface.html")

