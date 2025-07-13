from django.urls import path
from . import views

urlpatterns = [
    path("", views.truckmanagement, name='truckmanagement'),
    path("driverdirectory/", views.driverdirectory, name='driverdirectory'),
    path('deletet/<int:id>/', views.delete_trucker, name='delete_trucker'),
    path('deletej/<int:id>/', views.delete_job, name='delete_job'),
    path("licenseplates/", views.licenseplates, name="licenseplates"),
]