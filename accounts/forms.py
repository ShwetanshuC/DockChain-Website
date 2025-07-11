# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
#from .models import Job

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)  # Add more if needed (e.g., "name")

"""class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['driver', 'license_plate']"""