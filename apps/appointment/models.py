# models.py
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default="Dental")

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("waiting", "Waiting"),
        ("confirmed", "Confirmed"),
    ]

    patient_name = models.CharField(max_length=120)
    patient_phone = models.CharField(max_length=20)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_date}"
