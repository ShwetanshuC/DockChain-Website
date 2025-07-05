from django.shortcuts import render, HttpResponse

def success(request): 
    return render(request, "success.html")
