from truckmanagement.models import LicensePlate 
from truckmanagement.models import trucker

def nav_items(request):
    nav_options = []
    display_job_start = False

    if request.user.is_authenticated:
        if request.user.groups.filter(name="Driver").exists():
            nav_options = [
                {"label": "Home", "url": "/driverinterface/"},
                {"label": "Delivery Schedule", "url": "/driver/deliveries/"},
            ]
        elif request.user.groups.filter(name="Trucking Company").exists():
            nav_options = [
                {"label": "Home", "url": "/truckmanagement/"},
                {"label": "Driver Directory", "url": "/truckmanagement/driverdirectory/"},
                {"label": "Fleet Identification", "url": "/truckmanagement/licenseplates/"},
            ]
            display_job_start = True
        elif request.user.groups.filter(name="Port").exists():
            nav_options = [
                {"label": "Home", "url": "/portinterface/"},
                {"label": "Incoming Trucks", "url": "/port/incoming/"},
                {"label": "Scheduling", "url": "/port/schedule/"},
            ]
        elif request.user.is_superuser:
            nav_options = [
                {"label": "Admin Panel", "url": "/admin/"},
            ]

    path = request.path
    center = None
    left = []
    

    license_plates = LicensePlate.objects.all()
    filtered_truckers = trucker.objects.filter(organization__in=[request.user.organization, "Independent"]).order_by('-date_posted') if request.user.is_authenticated else trucker.objects.all().order_by('-date_posted')
    print(filtered_truckers)
    for option in nav_options:
        if path.startswith(option["url"]):
            center = option
        else:
            left.append(option)

    # Sort left so "Home" appears first if it's not the center
    left_sorted = sorted(left, key=lambda x: 0 if x["label"] == "Home" else 1)

    if nav_options:
        center_item = center or nav_options[0]
        left_items = [item for item in nav_options if item != center_item]
    else:
        center_item = None
        left_items = []

    return {
        "center_item": center_item,
        "left_items": left_items,
        "license_plates": license_plates,
        "display_job_start": display_job_start,
        "filtered_truckers": filtered_truckers
    }