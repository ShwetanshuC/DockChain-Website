from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        base_template = "base.html"
    else:
        base_template = "index.html"
    return render(request, "home.html", {"conditionalhome": base_template})
