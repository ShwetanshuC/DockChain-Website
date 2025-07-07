from django.urls import path
from . import views

urlpatterns = [
    path("", views.truckmanagement, name='truckmanagement'),
    path("driverdirectory/", views.driverdirectory, name='driverdirectory'),
    path('delete/<int:id>/', views.delete_trucker, name='delete_trucker'),
    path("licenseplates/", views.licenseplates, name="licenseplates"),
    
]