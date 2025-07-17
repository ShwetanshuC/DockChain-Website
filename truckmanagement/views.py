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
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from EasyOCRCode import EasyOCR_test

import secrets

# defines mode of operation for demo: valid and invalid
demoMode = True

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
    if (not request.user.is_cargo_broker):
        driver_id = request.POST.get('driver')
        plate_id = request.POST.get('license_plate')
    port_location = request.POST.get('port_location')
    job_type = request.POST.get('job_type')
    cargo_id = request.POST.get('cargo_id')
    description = request.POST.get('description', 'No description provided')
    isForSignup = request.user.is_cargo_broker
    organization = request.user.organization

    if (not request.user.is_cargo_broker):
        if driver_id and plate_id:
            driver_obj = get_object_or_404(trucker, id=driver_id)
            plate_obj = get_object_or_404(LicensePlate, id=plate_id)
            Job.objects.create(driver=driver_obj, license_plate=plate_obj, port_location=port_location, job_type=job_type, cargo_id=cargo_id, description=description, forSignUp=isForSignup, organization=organization)
    else:
        Job.objects.create(driver=None, license_plate_id=None, port_location=port_location, job_type=job_type, cargo_id=cargo_id, description=description, forSignUp=isForSignup, organization=organization)
def is_trucking_company(user):
    return user.is_superuser or user.groups.filter(name='Trucking Company').exists()

def generate_random_password():
    return secrets.token_urlsafe(16)  # Generates a secure random password

'''@csrf_exempt
# @require_http_methods(["GET", "POST"])
def arduino_endpoint(request):
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print(f"Body: {request.body}")
    print(f"POST data: {request.POST}")
    print(f"GET data: {request.GET}")
    if request.method == "GET":
        print("Received GET request")
        value = request.GET.get("value")
        job_id = request.GET.get("job_id")
        match value:
            case "active_jobs":
                jobs = Job.objects.filter(status="InProgress").values()
                return JsonResponse(list(jobs), safe=False)
            
            case "securedJobs":
                jobs = Job.objects.filter(status="SecurityCleared").values()
                return JsonResponse(list(jobs), safe=False)
            
            case "plate_initial":
                if demoMode:
                    return_plate = (EasyOCR_test.folder_scan("./plates_for_ocr/ValidPlate_Initial"))[0]
                else:
                    return_plate = (EasyOCR_test.folder_scan("./plates_for_ocr/InvalidPlate_Initial"))[0]
                return JsonResponse({"plate": return_plate})
            
            case "plates_all":
                plates = LicensePlate.objects.all().values()
                return JsonResponse(list(plates), safe=False)

            case "plate_final":
                if demoMode:
                    return_plate = (EasyOCR_test.folder_scan("./plates_for_ocr/ValidPlate_Final"))[0]
                else:
                    return_plate = (EasyOCR_test.folder_scan("./plates_for_ocr/InvalidPlate_Final"))[0]
                return JsonResponse({"plate": return_plate})
            
            case "drivers":
                drivers = trucker.objects.all().values()
                return JsonResponse(list(drivers), safe=False)

            case "status":
                if not job_id:
                    return HttpResponseBadRequest()
                try:
                    return HttpResponse(Job.objects.get(id=job_id).status)
                except Job.DoesNotExist:
                    return HttpResponse("Not found", status=404)

            case "temp_finger":
                if not job_id:
                    return HttpResponseBadRequest()
                try:
                    return HttpResponse(Job.objects.get(id=job_id).temp_finger)
                except Job.DoesNotExist:
                    return HttpResponse("Not found", status=404)

            case _:
                return HttpResponse(status=400)

    # POST method
    field = request.POST.get("column")
    value = request.POST.get("message")

    if not all([job_id, field, value]):
        return HttpResponseBadRequest()

    try:
        job = Job.objects.get(id=job_id)
        setattr(job, field, value)  # Assume valid field; fail loudly if not
        job.save()
        return HttpResponse("OK")
    except Job.DoesNotExist:
        return HttpResponse("Not found", status=404)

'''
@login_required(login_url='/accounts/login/')
@user_passes_test(is_trucking_company, login_url='/accounts/unauthorized/')
def truckmanagement(request): 
    if request.user.is_cargo_broker:
        truckers = trucker.objects.filter(organization="Independent").order_by('-date_posted')
    else:
        truckers = trucker.objects.filter(organization=request.user.organization).order_by('-date_posted')
    jobs = Job.objects.filter(organization=request.user.organization).order_by('timestamp')
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
    if request.user.is_cargo_broker:
        truckers = trucker.objects.filter(organization="Independent").order_by('-date_posted')
    else:
        truckers = trucker.objects.filter(organization=request.user.organization).order_by('-date_posted')
    
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
        user_to_delete = None
        try:
            user_to_delete = get_object_or_404(User, first_name=trucker_to_delete.firstname.lower(), last_name=trucker_to_delete.lastname.lower())
        except Exception as e:
            print("no user")
        trucker_to_delete.delete()
        if (user_to_delete != None):
            user_to_delete.delete()
    return redirect('driverdirectory')

def delete_job(request, id):
    if request.method == 'POST':
        job_to_delete = get_object_or_404(Job, id=id)
        job_to_delete.delete()
    return redirect('truckmanagement')

def select_trucker(request, job_id):
    if request.method == 'POST':
        trucker_id = request.POST.get('trucker_id')
        job = get_object_or_404(Job, id=job_id)
        _trucker = get_object_or_404(trucker, id=trucker_id)
        job.driver = _trucker
        job.license_plate = LicensePlate.objects.get(plate_number=_trucker.truck_license, state=_trucker.state)
        job.save()
    return redirect('truckmanagement')

# View for license plates
def licenseplates(request):
    if request.user.is_cargo_broker:
        truckers = trucker.objects.filter(organization="Independent").order_by('-date_posted')
    else:
        truckers = trucker.objects.filter(organization=request.user.organization).order_by('-date_posted')
    license_plates = LicensePlate.objects.all().order_by('-date_added')
    locations = User.objects.filter(groups__name='Port').values_list('port_location', flat=True).distinct()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_plate':
            form = LicensePlateForm(request.POST)
            form.organization = request.user.organization
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
    return render(request, "licenseplates.html", {"truckers": truckers, 'locations': locations, 'license_plates': license_plates, 'form': form})


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

@login_required(login_url='/accounts/login/')
@user_passes_test(is_trucking_company, login_url='/accounts/unauthorized/')
def add_trucker(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        role = request.POST.get('role')
        organization = request.user.organization if request.user.is_authenticated else "None"
        cocacenatedorg = (organization.lower()).replace(" ", "")
        newpassword = generate_random_password()
        print("Generated password:", newpassword)

        trucker.objects.create(firstname=firstname, lastname=lastname, role=role, organization=organization)
        truckuser = User.objects.create_user(
            f"{firstname.lower()}.{lastname.lower()}@{cocacenatedorg}.com",
            newpassword,
        )
        truckuser.first_name = firstname
        truckuser.last_name = lastname
        truckuser.organization = organization
        truckuser.save()

        group = Group.objects.get(name="Driver")
        truckuser.groups.add(group)
        return redirect('new_trucker', user_id=truckuser.id, new_password=newpassword)

    return render(request, 'companytruckerform.html')
