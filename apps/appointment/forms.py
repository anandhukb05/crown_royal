# appointments/forms.py

from django import forms
from .models import Appointment
from django.utils import timezone

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['patient', 'phone', 'doctor', 'date', 'time', 'am_pm', 'reason']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason', 'status']

        widgets = {
            'doctor': forms.Select(attrs={'class':'form-select form-select-lg shadow-sm'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg shadow-sm'}) 
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Only for create (not edit)
            if not self.instance.pk:
                self.fields['date'].initial = timezone.now().date()

    

