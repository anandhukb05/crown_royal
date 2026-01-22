# forms.py
from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile
        fields = ['name', 'email', 'age', 'gender', 'phno',
                   'address', 'aadhaar_id', 'country', 'state', 'pincode']

    def clean_phno(self):
        phno = self.cleaned_data.get("phno")
        if PatientProfile.objects.filter(phno=phno).exists():
            raise forms.ValidationError("Phone number already exists.")
        return phno

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if PatientProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age <= 0:
            raise forms.ValidationError("Age must be a positive number.")
        return age
