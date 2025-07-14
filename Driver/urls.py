from django.urls import path
from . import views

urlpatterns = [
    path("", views.driver, name='driver'),
    path("start_job/<int:job_id>/", views.start_job, name='start_job'),
]