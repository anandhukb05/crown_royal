# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm


# 📌 List appointments
def appointment_list(request):
    appointments = Appointment.objects.all().order_by("appointment_date", "appointment_time")
    return render(request, "list.html", {
        "appointments": appointments
    })


# 📌 Add appointment
def appointment_add(request):
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("appointment_list")

    return render(request, "add.html", {"form": form})


# 📌 Delete appointment
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.delete()
    return redirect("appointment_list")


# 📌 Reschedule appointment
def appointment_reschedule(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appt)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.status = "waiting"  # reset status after reschedule
        obj.save()
        return redirect("appointment_list")

    return render(request, "reschedule.html", {
        "form": form,
        "appt": appt
    })


# 📌 Doctor confirms appointment
def appointment_confirm(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = "confirmed"
    appt.save()
    return redirect("appointment_list")
