from django.utils import timezone 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from truckmanagement.models import Job
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect

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
    jobs = Job.objects.filter(driver__firstname=request.user.first_name, driver__lastname=request.user.last_name).order_by('timestamp')
    active_jobs = jobs.filter(status__in=['InProgress', 'SecurityCleared', 'CargoPickedUp'])
    scheduled_jobs = jobs.filter(status__in=['Pending', 'Approved', 'Denied'])
    completed_jobs = jobs.filter(status='Completed')
    return render(request, "driverinterface.html", {
        "active_jobs": active_jobs,
        "scheduled_jobs": scheduled_jobs,
        "completed_jobs": completed_jobs
    })

def start_job(request, job_id):
    if request.method != 'POST':
        return redirect('driver')
    
    job = get_object_or_404(Job, id=job_id)
    if job.status == 'Approved' and job.target_timestamp > timezone.now():
        job.status = 'InProgress'
        job.save()
        return redirect('driver')
    else:
        return HttpResponse("Job cannot be started at this time.", status=400)  # or handle as needed
