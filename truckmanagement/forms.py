from django import forms
from .models import trucker
from .models import LicensePlate
from .models import Job

class TruckerForm(forms.ModelForm):
    class Meta:
        model = trucker
        fields = ['firstname', 'lastname', 'role']


class LicensePlateForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ['state', 'plate_number']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['driver', 'license_plate']
