from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from truckmanagement.models import Job
from django.utils import timezone
from django.shortcuts import get_object_or_404

import datetime

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
    jobs = Job.objects.filter(port_location=request.user.port_location).order_by('timestamp')
    active_jobs = jobs.filter(status__in=['InProgress', 'SecurityCleared', 'CargoPickedUp'])
    scheduled_jobs = jobs.filter(status__in=['Pending', 'Approved', 'Denied'])
    completed_jobs = jobs.filter(status='Completed')
    return render(request, "portinterface.html", {"active_jobs": active_jobs, "scheduled_jobs": scheduled_jobs, "completed_jobs": completed_jobs})

def approve_job(request, id):
    if (request.method != 'POST'):
        return redirect("port")
    job = get_object_or_404(Job, id=id)
    job.status = 'Approved'
    job.approval_timestamp = timezone.now()
    job.save()
    return redirect("port")


def deny_job(request, id):
    if (request.method != 'POST'):
        return redirect("port")
    job = get_object_or_404(Job, id=id)
    job.status = 'Denied'
    job.save()
    return redirect("port")

def timestamp_job(request, id):
    if (request.method != 'POST'):
        return redirect("port")
    job = get_object_or_404(Job, id=id)
    raw_timestamp = request.POST.get('target_timestamp')
    job.target_timestamp = datetime.datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    job.save()
    return redirect("port")

# Existing view for Port Operator (can be used for other purposes)
@user_passes_test(is_port_operator, login_url='/unauthorized/')
def port_operator_view(request):
    return render(request, "portinterface.html")


