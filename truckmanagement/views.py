from django.shortcuts import render, redirect
from .models import trucker
from .forms import TruckerForm

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
