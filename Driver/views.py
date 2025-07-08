from django.shortcuts import render

def driver(request): 
    return render(request, "driverinterface.html")