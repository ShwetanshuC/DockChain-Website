from django.http import JsonResponse
from truckmanagement.models import Job
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect

#sign up page
from .forms import CustomUserCreationForm
from .forms import PortUserCreationForm
from .forms import CompanyUserCreationForm
from truckmanagement.models import trucker
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import login
from truckmanagement.models import trucker

'''
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/truck_company_signup.html"
'''

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
    form_class = CompanyUserCreationForm
    template_name = "registration/truck_company_signup.html"
    # Remove success_url attribute since form_valid uses get_success_url
    def get_success_url(self):
        return "/truckmanagement/"

    def form_valid(self, form):
        print(form)
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        group = Group.objects.get(name="Trucking Company")
        user.groups.add(group)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        print(form)

# Port Operator Sign Up View
class PortSignUpView(CreateView):
    form_class = PortUserCreationForm
    template_name = "registration/port_signup.html"
    def get_success_url(self):
        return "/portinterface/"
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        
        group = Group.objects.get(name="Port")
        user.groups.add(group)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

# Distinct sign up views for each user role
class TruckDriverSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/driver_signup.html"

    def get_success_url(self):
        return "/driverinterface/"

    def form_valid(self, form):
        firstname = form.cleaned_data.get('first_name')
        lastname = form.cleaned_data.get('last_name')
        qualifications = form.cleaned_data.get('qualifications')
        role = "Independent Driver"
        organization = "Independent"
        truck_license = form.cleaned_data.get('truck_license')
        state = form.cleaned_data.get('state')
        trucker.objects.create(firstname=firstname, lastname=lastname, role=role, organization=organization, qualifications=qualifications, truck_license=truck_license, state=state)
        state = form.cleaned_data.get('state')
        truck_license = form.cleaned_data.get('truck_license')
        LicensePlate.objects.create(state=state, plate_number=truck_license, organization=organization)
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)

        user.organization = organization
        user.save()
        group = Group.objects.get(name="Driver")
        user.groups.add(group)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

def unauthorized_view(request):
    return render(request, "unauthorized.html", {"next": request.GET.get("next", "/")})


# Custom login view that redirects users to their respective interface after logging in
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = "/"

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="Driver").exists():
            return "/driverinterface/"
        elif user.groups.filter(name="Trucking Company").exists():
            return "/truckmanagement/"
        elif user.groups.filter(name="Port").exists():
            return "/portinterface/"
        elif user.is_superuser:
            return "/admin/"
        return super().get_success_url()
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def ManageProfile(request):
    return render(request, "manageprofile.html")


# Unified Live Search View
def unified_live_search(request):
    query = request.GET.get("q", "")
    trucker_results = []
    plate_results = []
    job_results = []

    if query:
        trucker_results = list(
            trucker.objects.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query) |
                Q(role__icontains=query)
            ).values("firstname", "lastname", "role")
        )

        plate_results = list(
            LicensePlate.objects.filter(
                Q(state__icontains=query) |
                Q(plate_number__icontains=query)
            ).values("state", "plate_number")
        )

        job_results = list(
            Job.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).values("title", "description")
        )

    return JsonResponse({
        "truckers": trucker_results,
        "license_plates": plate_results,
        "jobs": job_results
    })

def DriverDocumentation(request):
    return render(request, "driverDocumentation.html")

def PortDocumentation(request):
    return render(request, "portDocumentation.html")

def TruckCompanyDocumentation(request):
    return render(request, "truckCompanyDocumentation.html")
    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_username":
            new_username = request.POST.get("username")
            if new_username:
                user.username = new_username
                user.save()
                messages.success(request, "Username updated successfully.")

        elif action == "update_email":
            new_email = request.POST.get("email")
            if new_email:
                user.email = new_email
                user.save()
                messages.success(request, "Email updated successfully.")

        elif action == "change_password":
            # Placeholder for password change process
            messages.info(request, "Password change functionality coming soon.")

        elif action == "delete_account":
            logout(request)         # Log the user out first
            user.delete()           # Delete the user account
            return redirect("home") # Redirect to homepage

    return render(request, "manageprofile.html")
