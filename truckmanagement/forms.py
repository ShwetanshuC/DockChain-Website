from django import forms
from .models import trucker
from .models import LicensePlate

class TruckerForm(forms.ModelForm):
    class Meta:
        model = trucker
        fields = ['firstname', 'lastname', 'role']


class LicensePlateForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ['state', 'plate_number']