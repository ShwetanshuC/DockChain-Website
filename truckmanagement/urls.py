from django.urls import path
from . import views

urlpatterns = [
    path("", views.truckmanagement, name='truckmanagement'),
    path("driverdirectory/", views.driverdirectory, name='driverdirectory'),
]