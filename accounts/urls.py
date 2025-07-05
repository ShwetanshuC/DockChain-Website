from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path("success/", views.success, name='success'),
    path("signup/", SignUpView.as_view(), name="signup"),
]