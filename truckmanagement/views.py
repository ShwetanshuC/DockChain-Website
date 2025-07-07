from django.shortcuts import render, redirect
from .models import trucker
from .forms import TruckerForm
from django.shortcuts import get_object_or_404

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