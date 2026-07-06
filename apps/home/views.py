from django.shortcuts import render
from django.utils import timezone
from apps.patients.models import PatientProfile
from apps.appointment.models import Appointment
from crpms.branch_utils import branch_queryset

# Create your views here.


def home(request):
    today = timezone.now().date()

    today_appointments = branch_queryset(
        request, Appointment, date=today
    ).order_by('time')

    total_patients = branch_queryset(request, PatientProfile).count()

    return render(
            request,
            'home.html',
            {
                "total_patients": total_patients,
                "appointment_count_today": len(today_appointments),
                "today_appointments": today_appointments
            }
        )