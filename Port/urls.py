from django.urls import path
from . import views

urlpatterns = [
    path("", views.port, name='port'),
    path('approve_job/<int:id>/', views.approve_job, name='approve_job'),
    path('delete_job/<int:id>/', views.deny_job, name='deny_job'),
    path('timestamp_job/<int:id>/', views.timestamp_job, name='timestamp_job'),
]