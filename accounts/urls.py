from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path("success/", views.success, name='success'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("search/", views.search_truckers, name="search_truckers"),
    path("search_license_plates/", views.search_license_plates, name="search_license_plates"),
]