from django.shortcuts import render, HttpResponse

def success(request): 
    return render(request, "success.html")

#sign up page
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

from django.db.models import Q
from truckmanagement.models import trucker

def search_truckers(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = trucker.objects.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(role__icontains=query)
        )

    return render(request, "search_results.html", {"results": results, "query": query})