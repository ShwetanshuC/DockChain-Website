from django.shortcuts import render

def home(request):
    base_template = "base.html" if request.user.is_authenticated else "index.html"
    return render(request, "home.html", {"conditionalhome": base_template})