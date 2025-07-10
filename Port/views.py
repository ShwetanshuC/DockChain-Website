from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required

# Group-checking function for "Port Operator"
def is_port_operator(user):
    return user.is_superuser or user.groups.filter(name='Port').exists()

# Group-checking function for "Trucking Company"
def is_trucking_company(user):
    return user.is_superuser or user.groups.filter(name='Trucking Company').exists()


# View for Port Operator, restricted by group membership
@login_required(login_url='/login/')
@user_passes_test(is_port_operator, login_url='/unauthorized/')
def port(request):
    return render(request, "portinterface.html")


# Existing view for Port Operator (can be used for other purposes)
@user_passes_test(is_port_operator, login_url='/unauthorized/')
def port_operator_view(request):
    return render(request, "portinterface.html")

# Create your views here.


