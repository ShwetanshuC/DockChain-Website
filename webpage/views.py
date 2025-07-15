from django.shortcuts import render
from truckmanagement.views import createjob
from truckmanagement.models import Job

def home(request):
    if request.user.is_authenticated:
        base_template = "base.html"
    elif request.method == 'POST' and request.POST.get('action') == 'start_job':
        createjob(request)
    else:
        base_template = "index.html"
    return render(request, "home.html", {"conditionalhome": base_template})