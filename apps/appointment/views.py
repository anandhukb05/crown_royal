# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from apps.patients.models import PatientProfile
from django.http import JsonResponse


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():

            patient_id = request.POST.get('patient')

            if not patient_id:
                form.add_error(None, "Please select a patient properly.")
            else:
                appointment = form.save(commit=False)
                appointment.patient = PatientProfile.objects.get(patient_id=patient_id)
                appointment.phone = appointment.patient.phno
                appointment.save()
                return redirect('appointment_list')

    else:
        form = AppointmentForm()

    return render(request, 'add.html', {'form': form})


def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            appointment = form.save(commit=False)

            patient_id = request.POST.get('patient')

            if patient_id:
                appointment.patient = PatientProfile.objects.get(patient_id=patient_id)
                appointment.phone = appointment.patient.phno

            appointment.save()
            return redirect('appointment_list')

    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'add.html', {
        'form': form,
        'selected_patient_name': appointment.patient.name,
        'selected_patient_id': appointment.patient.patient_id,
        'selected_phone': appointment.patient.phno,
    })


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('appointment_list')


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-date')

    search = request.GET.get('search')
    date = request.GET.get('date')

    if search:
        appointments = appointments.filter(
            Q(patient__name__icontains=search)
        )

    if date:
        appointments = appointments.filter(date=date)

    return render(request, 'list.html', {
        'appointments': appointments
    })

# patients/views.py


def patient_search(request):
    term = request.GET.get('term')
    patients = PatientProfile.objects.filter(name__icontains=term)[:10]

    data = []
    for p in patients:
        data.append({
            'id': p.patient_id,
            'name': p.name,
            'phone': p.phno
        })

    return JsonResponse(data, safe=False)