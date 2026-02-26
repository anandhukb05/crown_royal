# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm
from apps.patients.models import PatientProfile
from django.http import JsonResponse


def appointment_create(request):
    form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('appointment_list')
            except:
                form.add_error(None, "Doctor already has appointment on this date.")

    return render(request, 'add.html', {'form': form})


def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(instance=appointment)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')

    return render(request, 'add.html', {'form': form})


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