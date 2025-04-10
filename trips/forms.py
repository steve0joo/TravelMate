from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'destination', 'start_date', 'end_date', 'trip_type']
        widgets = {
                'start_date': forms.DateInput(attrs={'type': 'date'}),
                'end_date': forms.DateInput(attrs={'type': 'date'}),
                'trip_type': forms.Select(attrs={'class': 'input-field'})
            }