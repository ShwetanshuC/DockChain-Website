from truckmanagement.models import LicensePlate 
from truckmanagement.models import trucker

def nav_items(request):
    nav_options = [
        {"label": "Home", "url": "/truckmanagement/"},
        {"label": "Driver Directory", "url": "/truckmanagement/driverdirectory/"},
        {"label": "Fleet identification", "url": "/truckmanagement/licenseplates/"}
    ]

    path = request.path
    center = None
    left = []
    

    license_plates = LicensePlate.objects.all()
    truckers = trucker.objects.all()

    for option in nav_options:
        if path.startswith(option["url"]):
            center = option
        else:
            left.append(option)

    # Sort left so "Home" appears first if it's not the center
    left_sorted = sorted(left, key=lambda x: 0 if x["label"] == "Home" else 1)

    return {
        "center_item": center or nav_options[0],
        "left_items": [item for item in nav_options if item != (center or nav_options[0])],
        "license_plates": license_plates,
        "truckers": truckers
    }