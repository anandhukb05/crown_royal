# forms.py
from django import forms
from .models import PatientProfile

from django import forms
from .models import PatientProfile


class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile
        fields = [
            'name', 'email', 'age', 'gender', 'phno',
            'address', 'aadhaar_id', 'country', 'state', 'pincode'
        ]

    def clean_phno(self):
        phno = self.cleaned_data.get("phno")

        qs = PatientProfile.objects.filter(phno=phno)

        # Exclude current instance when editing
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Phone number already exists.")

        return phno


    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = PatientProfile.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Email already exists.")

        return email


    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age <= 0:
            raise forms.ValidationError("Age must be a positive number.")

        return age
