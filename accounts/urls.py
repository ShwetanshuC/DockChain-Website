from django.urls import path
from . import views
from .views import (
    SignUpView,
    TruckDriverSignUpView,
    TruckCompanySignUpView,
    PortSignUpView,
    CustomLoginView,
    ManageProfile
)

urlpatterns = [
    path("signup/driver/", TruckDriverSignUpView.as_view(), name="signup_driver"),
    path("signup/company/", TruckCompanySignUpView.as_view(), name="signup_company"),
    path("signup/port/", PortSignUpView.as_view(), name="signup_port"),
    path("search/", views.search_truckers, name="search_truckers"),
    path("search_license_plates/", views.search_license_plates, name="search_license_plates"),
    path("unauthorized/", views.unauthorized_view, name="unauthorized"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("manageprofile/", views.ManageProfile, name="manageprofile"),
    #Below this is all the documentation stuff----------------------------
    path("driverDocumentation/", views.DriverDocumentation, name="DriverDocumentation"),
    path("portDocumentation/", views.PortDocumentation, name="PortDocumentation"),
    path("truckCompanyDocumentation/", views.TruckCompanyDocumentation, name="TruckCompanyDocumentation"),

]