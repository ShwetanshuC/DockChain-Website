from django.shortcuts import render, HttpResponse

def success(request): 
    return render(request, "success.html")

#sign up page
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/truck_company_signup.html"


# Distinct sign up views for each user role
class TruckDriverSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/driver_signup.html"

class TruckCompanySignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/truck_company_signup.html"

class PortSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/port_signup.html"

from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import login
from truckmanagement.models import trucker

def search_truckers(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = trucker.objects.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(role__icontains=query)
        )

    return render(request, "search_results.html", {"results": results, "query": query})

from truckmanagement.models import LicensePlate  # adjust the model name if needed
from truckmanagement.forms import LicensePlateForm  # Ensure this import is present

def search_license_plates(request):
    query = request.GET.get("q")
    license_plates = []

    if query:
        license_plates = LicensePlate.objects.filter(
            Q(state__icontains=query) |
            Q(plate_number__icontains=query)
        )

    form = LicensePlateForm()
    return render(request, "licenseplates.html", {
        "license_plates": license_plates,
        "query": query,
        "form": form
    })


# Trucking Company Sign Up View
class TruckCompanySignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/truck_company_signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name="Trucking Company")
        user.groups.add(group)
        login(self.request, user)
        return super().form_valid(form)
    

# Port Operator Sign Up View
class PortSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/port_signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name="Port")
        user.groups.add(group)
        return super().form_valid(form)

# TruckDriverSignUpView: Assigns new users to the "Driver" group and logs them in.
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm

class TruckDriverSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/driver_signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name="Driver")
        user.groups.add(group)
        login(self.request, user)
        return super().form_valid(form)