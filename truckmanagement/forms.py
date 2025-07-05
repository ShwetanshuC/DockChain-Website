from django import forms
from .models import trucker

class TruckerForm(forms.ModelForm):
    class Meta:
        model = trucker
        fields = ['name', 'description']