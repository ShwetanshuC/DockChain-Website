from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from .models import trucker, LicensePlate, Job
from .forms import TruckerForm, LicensePlateForm, JobForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login

def trucker_list(request):
    truckers = trucker.objects.all().order_by('-date_posted')
    return render(request, 'trucker_list.html', {'truckers': truckers})

def add_job(request):
    if request.method == 'POST':
        form = TruckerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trucker_list')
    else:
        form = TruckerForm()
    return render(request, 'interface1.html', {'form': form})

def is_trucking_company(user):
    return user.is_superuser or user.groups.filter(name='Trucking Company').exists()

@login_required(login_url='/accounts/login/')
@user_passes_test(is_trucking_company, login_url='/accounts/unauthorized/')
def truckmanagement(request): 
    truckers = trucker.objects.all().order_by('-date_posted')
    
    if request.method == 'POST':
        form = TruckerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truckmanagement')
    else:
        form = TruckerForm()

    return render(request, "interface1.html", {'truckers': truckers, 'form': form})

def driverdirectory(request): 
    truckers = trucker.objects.all().order_by('-date_posted')
    
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
            trucker.objects.create(firstname=firstname, lastname=lastname, role=role)
            return redirect('driverdirectory')

    else:
        form = TruckerForm()

    return render(request, "driverdirectory.html", {'truckers': truckers, 'form': TruckerForm()})

def delete_trucker(request, id):
    if request.method == 'POST':
        trucker_to_delete = get_object_or_404(trucker, id=id)
        trucker_to_delete.delete()
    return redirect('driverdirectory')


# View for license plates
def licenseplates(request):
    license_plates = LicensePlate.objects.all().order_by('-date_added')

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

    form = LicensePlateForm()
    return render(request, "licenseplates.html", {'license_plates': license_plates, 'form': form})


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
