# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "qualifications")  # Add more if needed (e.g., "name")

class PortUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "port_location",)  # Add more if needed (e.g., "name")

class CompanyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "organization", "isCargoBroker", "services")  # Add more if needed (e.g., "name")