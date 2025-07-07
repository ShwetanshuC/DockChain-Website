def nav_items(request):
    return {
        "nav_items": [
            {"label": "Home", "center": request.path == "/"},
            {"label": "Driver Directory", "center": request.path.startswith("/truckmanagement/driverdirectory")}
        ]
    }