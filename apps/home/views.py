from django.shortcuts import render
from apps.patients.models import PatientProfile
# Create your views here.


def home(request):
    total_patients = PatientProfile.objects.count()
    return render(
            request,
            'home.html',
            {"total_patients": total_patients}
        )