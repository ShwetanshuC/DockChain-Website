from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from .models import trucker, LicensePlate, Job
from .forms import TruckerForm, LicensePlateForm, JobForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login

import secrets

def trucker_list(request):
    truckers = trucker.objects.all().order_by('-date_posted')
    return render(request, 'trucker_list.html', {'truckers': truckers})

"""def add_job(request):
    if request.method == 'POST':
        form = TruckerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trucker_list')
    else:
        form = TruckerForm()
    return render(request, 'interface1.html', {'form': form})"""


#elif action == 'start_job':
    #createjob(request)
    #return redirect('driverdirectory')
def createjob(request):
    driver_id = request.POST.get('driver')
    plate_id = request.POST.get('license_plate')
    port_location = request.POST.get('port_location')
    job_type = request.POST.get('job_type')
    cargo_id = request.POST.get('cargo_id')
    description = request.POST.get('description', 'No description provided')

    if driver_id and plate_id:
        driver_obj = get_object_or_404(trucker, id=driver_id)
        plate_obj = get_object_or_404(LicensePlate, id=plate_id)
        Job.objects.create(driver=driver_obj, license_plate=plate_obj, port_location=port_location, job_type=job_type, cargo_id=cargo_id, description=description)

def is_trucking_company(user):
    return user.is_superuser or user.groups.filter(name='Trucking Company').exists()

def generate_random_password():
    return secrets.token_urlsafe(16)  # Generates a secure random password

@login_required(login_url='/accounts/login/')
@user_passes_test(is_trucking_company, login_url='/accounts/unauthorized/')
def truckmanagement(request): 
    truckers = trucker.objects.all().order_by('-date_posted')
    jobs = Job.objects.all().order_by('timestamp')
    active_jobs = jobs.filter(status__in=['InProgress', 'SecurityCleared', 'CargoPickedUp'])
    scheduled_jobs = jobs.filter(status__in=['Pending', 'Approved', 'Denied'])
    completed_jobs = jobs.filter(status='Completed')
    locations = User.objects.filter(groups__name='Port').values_list('port_location', flat=True).distinct()
    if jobs:
        print("Testing job_type:", jobs[0].job_type)
    if request.method == 'POST':
        if request.POST.get('action') == 'start_job':
            createjob(request)
            return redirect('truckmanagement')
        else:
            form = TruckerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('truckmanagement')
    else:
        form = TruckerForm()

    return render(request, "interface1.html", {'truckers': truckers, 'jobs': jobs, 'active_jobs': active_jobs, 'scheduled_jobs': scheduled_jobs, 'completed_jobs': completed_jobs, 'locations': locations, 'form': form})

def driverdirectory(request): 
    truckers = trucker.objects.all().order_by('-date_posted')
    locations = User.objects.filter(groups__name='Port').values_list('port_location', flat=True).distinct()
    
    if request.method == 'POST':
        print("POST ACTION:", request.POST.get('action'))
        print("EDIT ID:", request.POST.get('edit_id'))
        action = request.POST.get('action')

        if action == 'edit':
            edit_id = request.POST.get('edit_id')
            t = get_object_or_404(trucker, id=edit_id)
            t.firstname = request.POST.get('firstname')
            t.lastname = request.POST.get('lastname')
            t.role = request.POST.get('role')
            t.save()
            return redirect('driverdirectory')

        elif action == 'add':
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            role = request.POST.get('role')
            organization = request.user.organization if request.user.is_authenticated else "None"
            qualifications="none"
            cocacenatedorg = (organization.lower()).replace(" ", "")
            newpassword = generate_random_password()
            print("Generated password:", newpassword)
            trucker.objects.create(firstname=firstname, lastname=lastname, role=role, organization=organization, qualifications=qualifications)
            truckuser = User.objects.create_user(
                f"{firstname.lower()}.{lastname.lower()}@{cocacenatedorg}.com",
                newpassword,
            )

            truckuser.first_name = firstname
            truckuser.last_name = lastname
            truckuser.organization = organization
            truckuser.qualifications = qualifications
            truckuser.save()

            group = Group.objects.get(name="Driver")
            truckuser.groups.add(group)
            return redirect('new_trucker', user_id=truckuser.id, new_password=newpassword)

        elif action == 'start_job':
            createjob(request)
            return redirect('driverdirectory')

    else:
        form = TruckerForm()

    return render(request, "driverdirectory.html", {'truckers': truckers, 'locations': locations, 'form': TruckerForm()})

def new_trucker(request, user_id, new_password):
    truck_user = get_object_or_404(User, id=user_id)
    return render(request, "new_trucker.html", {'truck_user': truck_user, 'new_password': new_password})

def delete_trucker(request, id):
    if request.method == 'POST':
        trucker_to_delete = get_object_or_404(trucker, id=id)
        trucker_to_delete.delete()
    return redirect('driverdirectory')

def delete_job(request, id):
    if request.method == 'POST':
        job_to_delete = get_object_or_404(Job, id=id)
        job_to_delete.delete()
    return redirect('truckmanagement')

# View for license plates
def licenseplates(request):
    license_plates = LicensePlate.objects.all().order_by('-date_added')
    locations = User.objects.filter(groups__name='Port').values_list('port_location', flat=True).distinct()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_plate':
            form = LicensePlateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('licenseplates')

        elif action == 'edit_plate':
            plate_id = request.POST.get('plate_id')
            plate = get_object_or_404(LicensePlate, id=plate_id)
            plate.state = request.POST.get('state')
            plate.plate_number = request.POST.get('plate_number')
            plate.save()
            return redirect('licenseplates')

        elif action == 'delete_plate':
            plate_id = request.POST.get('plate_id')
            plate = get_object_or_404(LicensePlate, id=plate_id)
            plate.delete()
            return redirect('licenseplates')
        
        elif action == 'start_job':
            createjob(request)
            return redirect('licenseplates')

    form = LicensePlateForm()
    return render(request, "licenseplates.html", {'locations': locations, 'license_plates': license_plates, 'form': form})


#start job
def start_job(request):
    if request.method == 'POST' and request.POST.get('action') == 'start_job':
        driver_id = request.POST.get('trucker_id')
        plate_id = request.POST.get('plate_id')

        print(driver_id, plate_id)

        if driver_id and plate_id:
            driver_obj = get_object_or_404(trucker, id=driver_id)
            plate_obj = get_object_or_404(LicensePlate, id=plate_id)
            form = JobForm(driver=driver_obj, license_plate=plate_obj)
            if form.is_valid():
                form.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))
