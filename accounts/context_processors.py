def nav_items(request):
    path = request.path
    if path == "/truckmanagement/":
        center = {"label": "Home", "url": "/truckmanagement/"}
        left = [{"label": "Driver Directory", "url": "/truckmanagement/driverdirectory/"}]
    elif path.startswith("/truckmanagement/driverdirectory"):
        center = {"label": "Driver Directory", "url": "/truckmanagement/driverdirectory/"}
        left = [{"label": "Home", "url": "/truckmanagement/"}]
    else:
        center = {"label": "Home", "url": "/truckmanagement/"}
        left = [{"label": "Driver Directory", "url": "/truckmanagement/driverdirectory/"}]

    return {
        "center_item": center,
        "left_items": left
    }